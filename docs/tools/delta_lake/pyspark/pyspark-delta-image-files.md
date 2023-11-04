# Pyspark Delta lake Image Files

**Update**: `2023-05-16` |
**Tag**: `Python` `Spark` `Delta Lake` `Image Files`

## Limitations

If you have very large images, use delta table containing path to the file rather
than ingesting the image in binary file format.

> **Warning**: \
> **Binary file format can support up to 2 GB per image.** In general, if your image
> files are larger than 512 MB, we recommend storing the path to the file in the
> table rather than storing the content/data of image file itself.
