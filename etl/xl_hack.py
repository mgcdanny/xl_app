
from zipfile import ZipFile, ZIP_DEFLATED
filename = "../upload/Intake_simple.xlsx"
archive = ZipFile(filename, 'r', ZIP_DEFLATED)
archive.extractall("test_extract/")
#wb = Workbook(guess_types=guess_types, data_only=data_only)
# _load_workbook(wb, archive, filename, use_iterators, keep_vba)




