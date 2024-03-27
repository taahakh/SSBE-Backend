# import unittest
# import json
# from unittest.mock import Mock, patch
# from model_interface import SummaryType
# from servicemanager import SummarisationManager

# class TestSummarisationManager(unittest.TestCase):

#     def setUp(self):
#         self.sum_manager = SummarisationManager()

#     def test_create_model_descriptors(self):
#         # Mocking model_list with sample data
#         self.sum_manager.model_list = {
#             "model1": Mock(model_name="Model1", text_type=["text1", "text2"], summary_type=SummaryType.ABSTRACTIVE, description="Description1", minimum_summary_length=50, maximum_summary_length=100),
#             "model2": Mock(model_name="Model2", text_type=["text3", "text4"], summary_type=SummaryType.EXTRACTIVE, description="Description2", minimum_summary_length=30, maximum_summary_length=70)
#         }
        
#         # Test create_model_descriptors method
#         self.sum_manager.create_model_descriptors()

#         # Check if md.json file is created with correct data
#         with open('md.json', 'r') as file:
#             descriptor_list = json.load(file)
#             self.assertEqual(len(descriptor_list), 2)  # Check if two descriptors are created

#             # Check if each model descriptor is created correctly
#             self.assertEqual(descriptor_list[0]["model-name"], "Model1")
#             self.assertEqual(descriptor_list[0]["text-type"], ["text1", "text2"])
#             self.assertEqual(descriptor_list[0]["summary-type"], "ab")
#             self.assertEqual(descriptor_list[0]["description"], "Description1")
#             self.assertEqual(descriptor_list[0]["summary-length"]["min"], 50)
#             self.assertEqual(descriptor_list[0]["summary-length"]["max"], 100)

#             self.assertEqual(descriptor_list[1]["model-name"], "Model2")
#             self.assertEqual(descriptor_list[1]["text-type"], ["text3", "text4"])
#             self.assertEqual(descriptor_list[1]["summary-type"], "ex")
#             self.assertEqual(descriptor_list[1]["description"], "Description2")
#             self.assertEqual(descriptor_list[1]["summary-length"]["min"], 30)
#             self.assertEqual(descriptor_list[1]["summary-length"]["max"], 70)

#     @patch('builtins.open', create=True)
#     def test_load_resources(self, mock_open):
#         # Mocking file read
#         mock_open.return_value.__enter__.return_value.read.return_value = ['model1', 'model2']

#         # Test load_resources method
#         self.sum_manager.load_resources()

#         # Check if model_list is populated correctly
#         self.assertEqual(len(self.sum_manager.model_list), 2)
#         self.assertIn("Model1", self.sum_manager.model_list)
#         self.assertIn("Model2", self.sum_manager.model_list)

#     def test_model_loader(self):
#         # Mocking load_model method
#         mock_model = Mock()
#         mock_model.load_model = Mock()
#         self.sum_manager.model_list["Model1"] = mock_model

#         # Test model_loader method
#         self.sum_manager.model_loader("Model1")

#         # Check if load_model is called
#         mock_model.load_model.assert_called_once()

#     def test_is_model_abstractive(self):
#         # Mocking model_list with a sample model
#         mock_model = Mock(summary_type=SummaryType.ABSTRACTIVE)
#         self.sum_manager.model_list["Model1"] = mock_model

#         # Test is_model_abstractive method
#         self.assertTrue(self.sum_manager.is_model_abstractive("Model1"))

#     @patch.object(SummarisationManager, 'model_loader')
#     def test_summarise(self, mock_model_loader):
#         # Mocking model_loader method
#         mock_model_loader.return_value = Mock(summarise=Mock(return_value=(True, "Summary")))

#         # Test summarise method
#         result = self.sum_manager.summarise("Text", "Model1", 50)

#         # Check if model_loader is called
#         mock_model_loader.assert_called_once_with("Model1")

#         # Check if summarise returns correct output
#         self.assertEqual(result, "Summary")

# if __name__ == '__main__':
#     unittest.main()
