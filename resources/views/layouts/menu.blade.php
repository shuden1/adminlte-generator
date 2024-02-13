<li class="nav-item">
    <a href="{{ route('companies.index') }}"
       class="nav-link {{ Request::is('companies*') ? 'active' : '' }}">
        <p>Companies</p>
    </a>
</li>


<li class="nav-item">
    <a href="{{ route('decisionMakers.index') }}"
       class="nav-link {{ Request::is('decisionMakers*') ? 'active' : '' }}">
        <p>Decision Makers</p>
    </a>
</li>


<li class="nav-item">
    <a href="{{ route('jobs.index') }}"
       class="nav-link {{ Request::is('jobs*') ? 'active' : '' }}">
        <p>Jobs</p>
    </a>
</li>
<li class="nav-item">
    <a href="{{ route('suitableTitles.index') }}"
       class="nav-link {{ Request::is('suitableTitles*') ? 'active' : '' }}">
        <p>Suitable Titles</p>
    </a>
</li>


