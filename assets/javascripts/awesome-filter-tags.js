const search_tags = ["dataset", "capacitydata", "map", "report"];

function filter_li_by_tag(select_tag) {

    const firstDiv = document.querySelector('div.tabbed-block');
    allProcesses = firstDiv.querySelectorAll('li');
    if (select_tag == "All") {
        allProcesses.forEach(li => {
            li.style.display = 'list-item';
        });
    } else {
        // Hide all li-elements
        allProcesses.forEach(li => {
            li.style.display = 'none';
        });

        // Show li-elements filtered
        processesWithDate = Array.from(allProcesses).filter(li =>
        li.querySelector('span.meta-' + select_tag) );
        processesWithDate.forEach(li => {
            li.style.display = 'list-item';
        });
    }

    // Manage filter button style
    for (const stag of ["All"].concat(search_tags)) {
        mybtn = document.getElementById("filter-button-" + stag);
        if (stag != select_tag) {
            mybtn.className = "tag-filter__bar";
        } else {
            mybtn.className = "tag-filter__bar is-active";
        }

    }

}

function show_buttons_for_filter_tag() {

    TYPE_EMOJI = {
        "dataset": "📊",
        "report": "📄",
        "map": "🗺️",
        "capacitydata": "📦",
        "date": "📅",
        "license": "⚖️",
        "All": "",
    }


    const filtersHost =
    document.getElementById("tag-filters") ||
    document.querySelector("main") ||
    document.body;

    filtersHost.style.display = "flex";

    for (const stag of ["All"].concat(search_tags)) {

        const ui = document.createElement("div");
                if (stag=="All") {
        ui.className = "tag-filter__bar is-active";
                } else {
                    ui.className = "tag-filter__bar";
                }
        ui.id = "filter-button-" + stag;


        const allBtn = document.createElement("button");
        allBtn.textContent = TYPE_EMOJI[stag] + " " + stag;
        allBtn.tag = stag;
        allBtn.className = "tag-filter__pill";
        ui.appendChild(allBtn);

        filtersHost.appendChild(ui);

        allBtn.addEventListener("click", function () {
            console.log("Call of " + allBtn.tag);
            filter_li_by_tag(allBtn.tag);
        });

    }
}

