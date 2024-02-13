<?php

namespace App\Http\Controllers;

use App\Http\Requests\CreateDecisionMakerRequest;
use App\Http\Requests\UpdateDecisionMakerRequest;
use App\Repositories\DecisionMakerRepository;
use App\Http\Controllers\AppBaseController;
use Illuminate\Http\Request;
use Flash;
use Response;

class DecisionMakerController extends AppBaseController
{
    /** @var DecisionMakerRepository $decisionMakerRepository*/
    private $decisionMakerRepository;

    public function __construct(DecisionMakerRepository $decisionMakerRepo)
    {
        $this->decisionMakerRepository = $decisionMakerRepo;
    }

    /**
     * Display a listing of the DecisionMaker.
     *
     * @param Request $request
     *
     * @return Response
     */
    public function index(Request $request)
    {
        $decisionMakers = $this->decisionMakerRepository->allWithNonDeletedCompanies();
        return view('decision_makers.index', compact('decisionMakers'));
    }

    public function indexForCompany($companyId)
    {
        $decisionMakers = $this->decisionMakerRepository->findByCompanyId($companyId);
        return view('decision_makers.table', compact('decisionMakers'));
    }

    /**
     * Show the form for creating a new DecisionMaker.
     *
     * @return Response
     */
    public function create()
    {
        return view('decision_makers.create');
    }

    /**
     * Store a newly created DecisionMaker in storage.
     *
     * @param CreateDecisionMakerRequest $request
     *
     * @return Response
     */
    public function store(CreateDecisionMakerRequest $request)
    {
        $input = $request->all();

        $decisionMaker = $this->decisionMakerRepository->create($input);

        Flash::success('Decision Maker saved successfully.');

        return redirect(route('decisionMakers.index'));
    }

    /**
     * Display the specified DecisionMaker.
     *
     * @param int $id
     *
     * @return Response
     */
    public function show($id)
    {
        $decisionMaker = $this->decisionMakerRepository->find($id);

        if (empty($decisionMaker)) {
            Flash::error('Decision Maker not found');

            return redirect(route('decisionMakers.index'));
        }

        return view('decision_makers.show')->with('decisionMaker', $decisionMaker);
    }

    /**
     * Show the form for editing the specified DecisionMaker.
     *
     * @param int $id
     *
     * @return Response
     */
    public function edit($id)
    {
        $decisionMaker = $this->decisionMakerRepository->find($id);

        if (empty($decisionMaker)) {
            Flash::error('Decision Maker not found');

            return redirect(route('decisionMakers.index'));
        }

        return view('decision_makers.edit')->with('decisionMaker', $decisionMaker);
    }

    /**
     * Update the specified DecisionMaker in storage.
     *
     * @param int $id
     * @param UpdateDecisionMakerRequest $request
     *
     * @return Response
     */
    public function update($id, UpdateDecisionMakerRequest $request)
    {
        $decisionMaker = $this->decisionMakerRepository->find($id);

        if (empty($decisionMaker)) {
            Flash::error('Decision Maker not found');

            return redirect(route('decisionMakers.index'));
        }

        $decisionMaker = $this->decisionMakerRepository->update($request->all(), $id);

        Flash::success('Decision Maker updated successfully.');

        return redirect(route('decisionMakers.index'));
    }

    /**
     * Remove the specified DecisionMaker from storage.
     *
     * @param int $id
     *
     * @throws \Exception
     *
     * @return Response
     */
    public function destroy($id)
    {
        $decisionMaker = $this->decisionMakerRepository->find($id);

        if (empty($decisionMaker)) {
            Flash::error('Decision Maker not found');

            return redirect(route('decisionMakers.index'));
        }

        $this->decisionMakerRepository->delete($id);

        Flash::success('Decision Maker deleted successfully.');

        return redirect(route('decisionMakers.index'));
    }
}
