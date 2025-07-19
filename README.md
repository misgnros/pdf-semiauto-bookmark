# pdf-semiauto-bookmark

`pdf-semiauto-bookmark` is a CLI tool that automatically generates editable bookmarks and sets them on PDF files.

## Installation

```bash
pip install git+https://github.com/misgnros/pdf-semiauto-bookmark.git
```

## Usage

Suppose your directory is as follows:

```
.
└── input.pdf
```

### Extracting bookmarks

You can extract bookmarks with the following command:

```bash
autobm read input.pdf
```

After this step, a markdown file containing bookmark information will be generated:

```
.
├── input.md
└── input.pdf
```

### Setting bookmarks

You can edit the generated markdown file as you like.

If the markdown file is in the proper format, you can set bookmarks with the following command:

```bash
autobm write input.md
```

After this step, a PDF file with bookmarks will be generated:

```
.
├── input.md
├── input.pdf
└── input_with_bookmark.pdf
```
