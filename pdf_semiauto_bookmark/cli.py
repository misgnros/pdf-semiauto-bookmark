from pathlib import Path
import pymupdf
import pymupdf4llm
import typer
from .pdf_to_bookmark_md import export_existing_bookmark, generate_bookmark_from_text
from .set_bookmark import set_bookmark
import traceback

app = typer.Typer()


@app.command()
def read(file: Path):
    # if len(sys.argv) != 2:
    #     typer.echo("Usage: pdf_semiauto_bookmark read <filename>", err=True)
    #     raise typer.Exit(code=1)

    if file.suffix.lower() != ".pdf":
        typer.echo("Error: The file must be a PDF.", err=True)
        raise typer.Exit(code=1)

    if not file.exists() or not file.is_file():
        typer.echo("Error: The file does not exist or is not a valid file.", err=True)
        raise typer.Exit(code=1)

    try:
        target_pdf = pymupdf.open(file)
        bookmark_list = target_pdf.get_toc()

        # case1: the PDF already has bookmarks
        exist_toc = True if bookmark_list else False
        if exist_toc:
            export_existing_bookmark(file, bookmark_list)
            return

        # case2: the PDF does not have bookmarks
        all_text = pymupdf4llm.to_markdown(target_pdf, page_chunks=True)
        generate_bookmark_from_text(file, all_text)

    except Exception as e:
        typer.echo(f"Error processing the PDF file: {e}", err=True)
        typer.echo(traceback.format_exc(), err=True)
        raise typer.Exit(code=1)


@app.command()
def write(file: Path):
    # if len(sys.argv) != 2:
    #     typer.echo("Usage: pdf_semiauto_bookmark write <filename>", err=True)
    #     raise typer.Exit(code=1)

    if file.suffix.lower() != ".md":
        typer.echo("Error: The file must be a Markdown.", err=True)
        raise typer.Exit(code=1)

    if not file.exists() or not file.is_file():
        typer.echo("Error: The file does not exist or is not a valid file.", err=True)
        raise typer.Exit(code=1)

    if not file.with_suffix(".pdf").exists():
        typer.echo("Error: The original PDF does not exist.", err=True)
        raise typer.Exit(code=1)

    try:
        set_bookmark(file)

    except Exception as e:
        typer.echo(f"Error processing the PDF file: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
