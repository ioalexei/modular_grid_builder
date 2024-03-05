# QGIS modular grid plugin
This plugin makes it easier to manage page layout guides in QGIS. 

The plugin lets you created a gridded layout to align layout items to, so that 
it's easier to create a balanced and aligned layout. 

## Installation

1. Download the [plugin zip file](https://github.com/ioalexei/modular_grid_builder/blob/main/modular_grid_builder.zip)
2. In QGIS, open Plugins menu > Manage and install plugins... 
3. In the Install from ZIP tab, use the file picker to select the downloaded zip file 
4. Click Install Plugin, then close the dialog
5. The plugin is now installed and can be found in Plugins > Modular Grid

## Usage 
The plugin dialog allows you to set the parameters to create a grid from. 

![Screenshot of plugin dialog](https://github.com/ioalexei/modular_grid_builder/blob/main/docs/screenshot_dialog_v0.1.png)

| Name | Description |
|------|-------------|
| Left margin | Amount of space to leave on left side of page before starting grid (in mm) | 
| Right margin | Amount of space to leave on right side of page before starting grid (in mm)|
| Top margin | Amount of space to leave from top of page before starting grid (in mm)| 
| Bottom margin | Amount of space to leave from bottom of page before starting grid (in mm)|
| Number of columns | Number of vertical divisions |  
| Number of rows | Number of horizontal divisions | 
| Gutter | Space between each row / column (in mm)| 
| Select page size | Select a page size from QGIS defaults | 
| Orientation | Select whether the page should be landscape or portrait | 
| Layout name | Give the layout a name (so you can identify it in the Layout Manager) | 

### Sample output 
This screenshot shows a sample output, using a landscape A4 page with 8 columns and 8 rows

![Screenshot of layout with modular grid](https://github.com/ioalexei/modular_grid_builder/blob/main/docs/screenshot_layout_v0.1.png)

## Contributing
Submit bugs and feature requests from the issues tab. Pull requests welcome. 

## License
[GNU Public License (GPL)](https://www.gnu.org/licenses/gpl-3.0.en.html)
