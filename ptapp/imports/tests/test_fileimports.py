##########################################
# Testing basic file import functionality.
##########################################
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO

from imports.ImportFileManagement import FileImporter
from imports.exceptions import FileImportException

from imports import models

################################################################################
# Test file importer functionality
###############################################################################
class TestFileImporter(TestCase):
    """ For testing FileImporterClass"""

    # Tests to write
    # account matching

    #-------------------------------------------------------------------------#
    def testDetectFileType(self):
        """ Verify that we can detect all the correct file types"""
        self.assertEqual(FileImporter.getFileType("file.qfx"), FileImporter.FILETYPE_QFX)
        self.assertEqual(FileImporter.getFileType("file.ofx"), FileImporter.FILETYPE_QFX)
        self.assertEqual(FileImporter.getFileType("file.QFX"), FileImporter.FILETYPE_QFX)
        self.assertEqual(FileImporter.getFileType("file.OFX"), FileImporter.FILETYPE_QFX)

        self.assertEqual(FileImporter.getFileType("file.noext"), FileImporter.FILETYPE_UNKNOWN)

    #--------------------------------------------------------------------------#
    def testCalculateFileHash(self):
        """ Verify we can correctly calculate the file hash"""
        ofxFilename = "bank.ofx"
        with open("imports/tests/fixtures/ofx/simple_bank.qfx", 'rb') as f:
            #Convert the file to a form as if it was uploaded to django
            upFile = SimpleUploadedFile(ofxFilename, f.read())

        fileHash = FileImporter.calculatefilehash(upFile)
        self.assertEqual(fileHash, "253126a389cb9a237a64c2d639b6e57c")
