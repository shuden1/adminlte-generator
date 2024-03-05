<?php

namespace App\Http\Controllers;

use App\Http\Requests\CreateSuitableTitleRequest;
use App\Http\Requests\UpdateSuitableTitleRequest;
use App\Repositories\SuitableTitleRepository;
use App\Http\Controllers\AppBaseController;
use Illuminate\Http\Request;
use Flash;
use Response;

class SuitableTitleController extends AppBaseController
{
    /** @var SuitableTitleRepository $suitableTitleRepository*/
    private $suitableTitleRepository;

    public function __construct(SuitableTitleRepository $suitableTitleRepo)
    {
        $this->suitableTitleRepository = $suitableTitleRepo;
    }

    /**
     * Display a listing of the SuitableTitle.
     *
     * @param Request $request
     *
     * @return Response
     */
    public function index(Request $request)
    {
        $suitableTitles = $this->suitableTitleRepository->all();

        return view('suitable_titles.index')
            ->with('suitableTitles', $suitableTitles);
    }

    /**
     * Show the form for creating a new SuitableTitle.
     *
     * @return Response
     */
    public function create()
    {
        return view('suitable_titles.create');
    }

    /**
     * Store a newly created SuitableTitle in storage.
     *
     * @param CreateSuitableTitleRequest $request
     *
     * @return Response
     */
    public function store(CreateSuitableTitleRequest $request)
    {
        $input = $request->all();

        $suitableTitle = $this->suitableTitleRepository->create($input);

        Flash::success('Suitable Title saved successfully.');

        auth()->user()->suitableTitles()->syncWithoutDetaching([$suitableTitle->id]);

        return redirect(route('suitableTitles.index'));
    }

    /**
     * Display the specified SuitableTitle.
     *
     * @param int $id
     *
     * @return Response
     */
    public function show($id)
    {
        $suitableTitle = $this->suitableTitleRepository->find($id);

        if (empty($suitableTitle)) {
            Flash::error('Suitable Title not found');

            return redirect(route('suitableTitles.index'));
        }

        return view('suitable_titles.show')->with('suitableTitle', $suitableTitle);
    }

    /**
     * Show the form for editing the specified SuitableTitle.
     *
     * @param int $id
     *
     * @return Response
     */
    public function edit($id)
    {
        $suitableTitle = $this->suitableTitleRepository->find($id);

        if (empty($suitableTitle)) {
            Flash::error('Suitable Title not found');

            return redirect(route('suitableTitles.index'));
        }

        return view('suitable_titles.edit')->with('suitableTitle', $suitableTitle);
    }

    /**
     * Update the specified SuitableTitle in storage.
     *
     * @param int $id
     * @param UpdateSuitableTitleRequest $request
     *
     * @return Response
     */
    public function update($id, UpdateSuitableTitleRequest $request)
    {
        $suitableTitle = $this->suitableTitleRepository->find($id);

        if (empty($suitableTitle)) {
            Flash::error('Suitable Title not found');

            return redirect(route('suitableTitles.index'));
        }

        $suitableTitle = $this->suitableTitleRepository->update($request->all(), $id);

        Flash::success('Suitable Title updated successfully.');

        return redirect(route('suitableTitles.index'));
    }

    /**
     * Remove the specified SuitableTitle from storage.
     *
     * @param int $id
     *
     * @throws \Exception
     *
     * @return Response
     */
    public function destroy($id)
    {
        $suitableTitle = $this->suitableTitleRepository->find($id);

        if (empty($suitableTitle)) {
            Flash::error('Suitable Title not found');

            return redirect(route('suitableTitles.index'));
        }

        $this->suitableTitleRepository->delete($id);

        Flash::success('Suitable Title deleted successfully.');

        return redirect(route('suitableTitles.index'));
    }
}
