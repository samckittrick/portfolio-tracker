##########################################
# Testing basic file import functionality.
##########################################
from django.test import TestCase
from io import BytesIO

from imports.ImportFileManagement import FileImporter
from imports.exceptions import FileImportException

################################################################################
# Test file importer functionality
###############################################################################
class TestFileImporter(TestCase):
    """ For testing FileImporterClass"""

    #-------------------------------------------------------------------------#
    def testUnknownFileType(self):
        self.assertRaises(FileImportException, FileImporter, "testfile.noext")

    #-------------------------------------------------------------------------#
    #def testDetectQFXWithOnlyFilename(self):
    #    f = FileImporter("mfile.ofx")

    #-------------------------------------------------------------------------#
    #def testDetectQFXWithFilenameAndFileObj(self):
    #    with open('imports/tests/fixtures/ofx/simple_bank.qfx', 'rb') as f:
    #        print(type(f))
    #        f = FileImporter("simple_bank.qfx", f)
    #        self.assertEqual(f.getFileType, FileImporter.FILETYPE_QFX)
