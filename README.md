# TEI Sourcer

Simple workflow to download METS XML records and transform them into TEI XML.

## What This Repo Contains

- `download_manifests.py`: Downloads METS XML files from a URL list.
- `manifest2tei.xml`: XSLT stylesheet to convert METS/MODS metadata to TEI.
- `build.xml`: Ant build targets for download and transformation.

## Requirements

- Python 3
- Java (for Saxon)
- Apache Ant

## Input

Create a file named `manifests.txt` in the project root, one METS XML URL per line, no delims.

## run ant, see outputs
- `manifests/`: downloaded METS XML files
- `tei/`: generated TEI XMLs
- `lib/`: downloaded Saxon JAR
