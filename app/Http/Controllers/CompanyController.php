<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessCompany;
use App\Jobs\RetrieveCompanyCareers;
use App\Models\Job;
use Facebook\WebDriver\Remote\DesiredCapabilities;
use Facebook\WebDriver\Remote\RemoteWebDriver;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Auth;
use OpenAI;
use OpenAI\Exceptions\ErrorException;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

use App\Http\Requests\CreateCompanyRequest;
use App\Http\Requests\UpdateCompanyRequest;
use App\Models\Company;
use App\Models\DecisionMaker;
use App\Repositories\CompanyRepository;
use App\Http\Controllers\AppBaseController;
use Illuminate\Http\Request;
use Laracasts\Flash\Flash;
use League\Csv\Reader;
use HeadlessChromium\Communication\Response;
use GuzzleHttp;

class CompanyController extends AppBaseController
{
    /** @var CompanyRepository $companyRepository*/
    private $companyRepository;

    public function __construct(CompanyRepository $companyRepo)
    {
        $this->companyRepository = $companyRepo;
    }

    /**
     * Display a listing of the Company.
     *
     * @param Request $request
     *
     * @return Response
     */
    public function index(Request $request)
    {
//        $companies = $this->companyRepository->all();
//        return view('companies.index')->with('companies', $companies);

        if (Auth::check()) { // Ensure there is an authenticated user
            $user = Auth::user(); // Get the authenticated user

            // Fetch companies associated with the authenticated user

            $sort = $request->get('sort', 'id'); // Default sort by 'id'
            $direction = $request->get('direction', 'asc'); // Default direction is 'asc'


            $companies = $user->companies()->orderBy($sort, $direction)->paginate(50);

            return view('companies.index', compact('companies', 'sort', 'direction'));
        } else {
            // Handle the case where there is no authenticated user, or redirect to login
            return redirect()->route('login')->with('error', 'You must be logged in to see this page.');
        }
    }

    /**
     * Show the form for creating a new Company.
     *
     * @return Response
     */
    public function create()
    {
        return view('companies.create');
    }

    /**
     * Show the form for uploading a new Company list.
     *
     * @return Response
     */
    public function upload()
    {
        return view('companies.upload');
    }

    public function import(Request $request)
    {
        $file = $request->file('file');
        $csv = Reader::createFromPath($file->getRealPath(), 'r');
        $csv->setHeaderOffset(0);
        // Assumes the first row in CSV is the header
        foreach ($csv as $record) {
            $company_existing = Company::where("careerPageUrl", $record["careerPageUrl"])->first();
            $exists = 0;
            if ($company_existing){
                $exists = 1;
            }
            $company = Company::where("careerPageUrl", $record["careerPageUrl"])->firstOr( function() use ($record) {

                $c = Company::create([
                    'name' => $record['company_name'],
                    'careerPageUrl' => $record['careerPageUrl'],
                    'linkedin_id' => $record['linkedin_id'],
                    'sauroned' => 1
                ]);
                return $c;
            });

            $company->name = $record['company_name'];
            $company->save();

            if (Auth::check()) { // Ensure there is an authenticated user
                $user = Auth::user(); // Get the authenticated user
                $user->companies()->syncWithoutDetaching($company->id); // Attach the new company to the user only if it's not already attached
            }

            if (!$exists) {

                $domain = parse_url($company->careerPageUrl, PHP_URL_HOST);
                $domain = str_replace('www.', '', $domain);

                if ($domain == "linkedin.com") {
                    ProcessCompany::dispatch($company, 0, 0);
                } else {
                    if (!file_exists("D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/scrape.py")) {
                        if ($record['has_jobs'] == 0) {
                            ProcessCompany::dispatch($company, 0, 0);
                        } else {
                            ProcessCompany::dispatch($company, 0, 1);
                        }
                    } else {
                        ProcessCompany::dispatch($company, 0, 1);
                    }
                }
                if (isset($record["first_name"])) {
                    DecisionMaker::firstOrCreate([
                        'company_id' => $company->id,
                        'firstName' => $record["first_name"],
                        'lastName' => $record["last_name"],
                        'profile_url' => rawurlencode($record["linkedin"]),
                        'email' => $record["email"]
                    ]);
                }
            }
        }

        return redirect(route('companies.index'));
    }

    /**
     * Store a newly created Company in storage.
     *
     * @param CreateCompanyRequest $request
     *
     * @return Response
     */
    public function store(CreateCompanyRequest $request)
    {
        $input = $request->all();

        $company = $this->companyRepository->create($input);

        Flash::success('Company saved successfully.');

        if (Auth::check()) { // Ensure there is an authenticated user
            $user = Auth::user(); // Get the authenticated user
            $user->companies()->attach($company->id); // Attach the new company to the user
        }

        //     Execute Python scripts after creating the company
        $domain = parse_url($company->careerPageUrl, PHP_URL_HOST);
        $domain = str_replace('www.', '', $domain);

        if (!file_exists("D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/scrape.py")) {
            ProcessCompany::dispatch($company, 0, 1);
        }

        // Run php artisan queue:work to launch the listener
        // Run php artisan websockets:serve to start websockets
        // npm run dev to generate js
        return redirect(route('companies.index'));
    }

    /**
     * Regenerate the script for the Company CareerPageUrl domain.
     *
     *
     * @return Response
     */
    public function regenerate($id, $unique)
    {
        $company = $this->companyRepository->find($id);

        ProcessCompany::dispatch($company, $unique, 1);

        // php artisan queue:work

        return redirect(route('companies.index'));
    }


    /**
     * Display the specified Company.
     *
     * @param int $id
     *
     * @return Response
     */
    public function show($id)
    {
        $company = Company::with('decisionMakers')->findOrFail($id);

        if (empty($company)) {
            Flash::error('Company not found');

            return redirect(route('companies.index'));
        }

        return view('companies.show')->with('company', $company);
    }

    /**
     * Show the form for editing the specified Company.
     *
     * @param int $id
     *
     * @return Response
     */
    public function edit($id)
    {
        $company = $this->companyRepository->find($id);

        if (empty($company)) {
            Flash::error('Company not found');

            return redirect(route('companies.index'));
        }

        return view('companies.edit')->with('company', $company);
    }

    /**
     * Update the specified Company in storage.
     *
     * @param int $id
     * @param UpdateCompanyRequest $request
     *
     * @return Response
     */
    public function update($id, UpdateCompanyRequest $request)
    {
        $company = $this->companyRepository->find($id);

        if (empty($company)) {
            Flash::error('Company not found');

            return redirect(route('companies.index'));
        }

        $company = $this->companyRepository->update($request->all(), $id);

        Flash::success('Company updated successfully.');

        return redirect(route('companies.index'));
    }

    public function getCompanyData($id)
    {
        $company = $this->companyRepository->find($id);
        return response()->json([
            'scripted' => $company->scripted,
            // Include any other data you might need
        ]);
    }


    /**
     * Remove the specified Company from storage.
     *
     * @param int $id
     *
     * @throws \Exception
     *
     * @return Response
     */
    public function destroy($id)
    {
        $company = $this->companyRepository->find($id);

        if (empty($company)) {
            Flash::error('Company not found');

            return redirect(route('companies.index'));
        }

        $this->companyRepository->delete($id);

        Flash::success('Company deleted successfully.');

        return redirect(route('companies.index'));
    }
}
