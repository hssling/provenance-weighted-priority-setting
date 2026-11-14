# Convert WHO's archived .rda snapshots to CSV, unchanged, for the stdlib-only analysis.
#
# The analysis in src/ and demos/ is pure Python; these files are R data, so
# R reads them once here and writes every data frame out whole. Nothing is
# selected, renamed, recoded or filtered: column names keep WHO's spelling
# (dots in the raw snapshots, underscores in the processed output) and the
# Python side maps them. Missing values are written as empty fields.
#
# Usage: Rscript tools/convert_vintages.R   (after tools/fetch_vintages.py)

args <- commandArgs(trailingOnly = FALSE)
here <- dirname(normalizePath(sub("^--file=", "", args[grep("^--file=", args)])))
root <- dirname(here)
raw <- file.path(root, "data", "vintages", "raw")
out <- file.path(root, "data", "vintages", "csv")
dir.create(out, showWarnings = FALSE, recursive = TRUE)

for (f in list.files(raw, pattern = "[.]rda$", full.names = TRUE)) {
  e <- new.env()
  objs <- load(f, envir = e)
  for (o in objs) {
    x <- as.data.frame(get(o, envir = e))
    dest <- file.path(out, paste0(sub("[.]rda$", "", basename(f)), "__", o, ".csv"))
    write.csv(x, dest, row.names = FALSE, na = "", fileEncoding = "UTF-8")
    cat(sprintf("%6d x %3d  %s\n", nrow(x), ncol(x), basename(dest)))
  }
}
