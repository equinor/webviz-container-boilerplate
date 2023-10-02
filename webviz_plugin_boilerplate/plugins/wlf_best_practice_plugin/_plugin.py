from typing import List

from dash import Input
from webviz_config import WebvizPluginABC
from webviz_config.utils import StrEnum

from ..._utils._data_model import DataModel
from ._shared_settings import DataNameSelection
from ._views._plot_view import GraphDataVisualization, GraphTypeSettings, PlotView
from ._views._plot_view._view_elements import GraphSettings, PlotViewElement
from ._views._table_view import TableOrderSelection, TableView
from ._views._table_view._view_elements import TableViewElement


class WlfBestPracticePlugin(WebvizPluginABC):
    """
    This Webviz plugin, to illustrate a best practice on code structure and how to
    separate code for clarity and usability when using the Webviz Layout Framework
    known as `WLF`.

    The plugin subclasses the abstract WebvizPluginABC base class, and implements
    the required subclasses for WLF - views, view elements and corresponding setting
    groups. Callback functionality is placed within the view objects.

    Shared settings are created at plugin level and slot inputs/states are provided
    for the views for use in callbacks.

    `Plugin functionality`:
    Plugin contains a model for data, which is populated with a set of mocked up data
    structures with unique names. The plugin provides radio items in shared setting for
    selecting a specific data source name from the set and show the data in a plot or
    a table. The views contain business logic for additional ad-hoc calculations (raw,
    reversed and flipped) for the selected data. Based on selected visualization in plot
    view the callback retrieves correct graph data from the model and provides it to the
    graph builder in the property serialization. Graph type options are provided (line
    plot and bar chart) as radio items for specifying which type of graphing should be
    used in the graph builder. When the graph is built, the builder can provide the JSON
    serialized result for the callback Output. As for the plot, the table retrieves the
    data from the model based on selection in shared settings. Further on the table view
    allows ascending or descending order of the data shown in the table.

    `Plugin folder/file structure:`
    * _shared_settings - Settings shared across the plugin views
    * _views - Views implemented for the plugin - plot and table
        *_plot_view
            *_view.py
            *_settings.py
            *_utils
                *_business_logic.py
                *_prop_serialization.py
            *_view_elements
                *_plot_view_element.py
                _settings.py
        *_table_view
            *_view.py
            *_settings.py
            *_utils
                *_business_logic.py
                *_prop_serialization.py
            *_view_elements
                *_table_view_element.py

    * Callbacks are placed within the `_view.py` files - Dash callbacks for handling user
    interaction and update of view.
    * _business_logic.py - Query database/input for relevant data and necessary
    ad-hoc calculations for data, separated from Dash specific code (no dash* import)
    * _prop_serialization.py - De-serializing and serializing callback property formats.
    Convert callback Input/State from JSON serializable property formats to strongly typed
    formats (de-serialize) for business logic. Create/build JSON serializable properties
    for Dash callback Output property by use of data from business logic.
    """

    class Ids(StrEnum):
        PLOT_VIEW = "plot-view"
        TABLE_VIEW = "table-view"

        SHARED_SETTINGS = "shared-settings"

    def __init__(
        self, screenshot_filename: str = "webviz-screenshot.png", _stretch: bool = False
    ) -> None:
        super().__init__(screenshot_filename, True)

        self._data_model = DataModel()
        self._data_model.populate_with_mock_data()

        self.settings_group = DataNameSelection()
        self.add_shared_settings_group(
            self.settings_group, WlfBestPracticePlugin.Ids.SHARED_SETTINGS
        )

        self.add_view(
            PlotView(
                self._data_model,
                slots=PlotView.Slots(
                    data_name_selector=Input(
                        self.settings_group.component_unique_id(
                            DataNameSelection.Ids.RADIO_ITEMS
                        ).to_string(),
                        "value",
                    )
                ),
            ),
            WlfBestPracticePlugin.Ids.PLOT_VIEW,
        )
        self.add_view(
            TableView(
                self._data_model,
                slots=TableView.Slots(
                    data_name_selector=Input(
                        self.settings_group.component_unique_id(
                            DataNameSelection.Ids.RADIO_ITEMS
                        ).to_string(),
                        "value",
                    )
                ),
            ),
            WlfBestPracticePlugin.Ids.TABLE_VIEW,
        )

    @property
    def tour_steps(self) -> List[dict]:
        return [
            {
                "id": self.view(WlfBestPracticePlugin.Ids.PLOT_VIEW)
                .view_element(PlotView.Ids.PLOT)
                .component_unique_id(PlotViewElement.Ids.GRAPH),
                "content": "Over here you see a plot that shows selected data set",
            },
            {
                "id": self.settings_group.component_unique_id(
                    DataNameSelection.Ids.RADIO_ITEMS
                ),
                "content": "Here you can change which data set you prefer.",
            },
            {
                "id": self.view(WlfBestPracticePlugin.Ids.PLOT_VIEW)
                .settings_group(PlotView.Ids.GRAPH_TYPE_SETTINGS)
                .component_unique_id(GraphTypeSettings.Ids.RADIO_ITEMS),
                "content": "...and here you can select which graph type you prefer.",
            },
            {
                "id": self.view(WlfBestPracticePlugin.Ids.PLOT_VIEW)
                .settings_group(PlotView.Ids.GRAPH_DATA_VISUALIZATION)
                .component_unique_id(GraphDataVisualization.Ids.RADIO_ITEMS),
                "content": "...furthermore you can select how to visualize the data values.",
            },
            {
                "id": self.view(WlfBestPracticePlugin.Ids.PLOT_VIEW)
                .view_element(PlotView.Ids.PLOT)
                .settings_group(PlotViewElement.Ids.GRAPH_SETTINGS)
                .component_unique_id(GraphSettings.Ids.RADIO_ITEMS),
                "content": "The plot contains settings which provides possibility to adjust "
                "graph colors.",
            },
            {
                "id": self.view(WlfBestPracticePlugin.Ids.TABLE_VIEW)
                .view_element(TableView.Ids.TABLE)
                .component_unique_id(TableViewElement.Ids.TABLE),
                "content": "There is also a table visualizing the data.",
            },
            {
                "id": self.view(WlfBestPracticePlugin.Ids.TABLE_VIEW)
                .settings_group(TableView.Ids.TABLE_ORDER_SELECTION)
                .component_unique_id(TableOrderSelection.Ids.RADIO_ITEMS),
                "content": "You can change the order of the table here.",
            },
        ]
