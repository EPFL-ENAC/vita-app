# Summarized inner working

`commands/gen_struct_out.py` is the entry point of the analysis. The OCR `.json` file is read to create a list of `DetectedText`, defined in `models/detected_text.py`, with information on the read text and the bounding boxes. Then, data is extracted from this list using a specific reader (for example, look at a definition in `readers/alcon_ex_500.json`). The reader rely on fuzzy string matching and relative positioning of bounding boxes (see `reader_scripts/search.py`).


# Software description file

The layout of documents rendered by any software can be described in a `.json` file placed inside the `readers` directory. The `.json` description file must have the following format:
```
{
	"name": string,
	"distinctive_pattern": regex,
	"fields": [
		...
	]
}
```
The `name` will be used to identify the software when using the `gen-struct-out` command. `distinctive_pattern` is a regex string uniquely identifying a document produced by the software.

## Fields description

### Required values
A field must at least contain the following:
```
{
	"name": string,
	"pattern": regex
}
```
`name` is used as an identifier when creating other fields placed in relation to this one. `pattern` is a regex string which may contain capture groups.


### Adding entries in structured output

To create entries from the capture groups of a field's regex, the names of the entries must be provided:
```
{
	...
	"keys": [string, string, ...],
}
```
By default, each key will be attributed to the regex capture groups in their appearing order. To change the capture groups corresponding to each key, add a `data_order` value (a list of integers). For example:
```
{
	...
	"keys": ["alpha", "bravo", "charlie"],
	"data_order": [1, 2, 0]
}
```
will add the entries `alpha: capture #1`, `bravo: capture #2`, `charlie: capture #0`.
All fields are added to the structured output in the order they appear in the `.json` file.


### Absolute positioning

To look for a field in a specific region of the image, add a region:
```
{
	...
	region: [xmin, xmax, ymin, ymax]
}
```
Coordinates are floating point numbers ranging from 0 to 1. The origin is located at the bottom left (y axis pointing upward). Regions are drawn in the images rendered by the `gen-struct-out` command for verification purposes.


### Relative positioning

To find a field positioned relatively to another, use the following syntax:
```
{
	...
	"relative_to": reference_name,
	"region": [xmin, xmax, ymin, ymax]
}
```
Coordinates are expressed relative to the center of the reference's bounding box and in units of this box's height.

Simplified syntaxes exist to define fields located on the right or below another one:
```
{
	...
	"on_right_of": reference_name,
	"region_width": number
},
{
	...
	"below": reference_name,
	"region_height": number
}
```
`region_width` and `region_height` are specified in units of the height of the reference's bounding box. If `region_width` is not specified, the whole horizontal space on the right of the reference is searched. If `region_height` is not specified, it is set to 1.


### Matching multiple candidates

If the text contained in one searched field is not unique, it may be needed to look for multiple occurrences of a single pattern by adding the following parameter:
```
{
	...
	"n_candidates": integer
}
```
This is useful when searching for a field that will serve as a reference for other relatively positioned fields.


## Regex patterns

Placeholders in the form of `{pattern.xxx}` may be used to avoid repetitions of regex patterns. Patterns are defined in `reader_scripts/patterns.py`. Other common patterns may be added there.
