import unittest
from unittest.mock import patch
import pandas as pd
from app_support import atlas_app


class InsightTests(unittest.TestCase):
    def test_insights_render_text_and_follow_dataset(self):
        from data import load_data
        samples = load_data().iloc[:2].copy()
        samples['status'] = ['Critically Endangered', 'Endangered']
        samples['ocean'] = ['Test Region', 'Test Region']
        samples['primary_threat'] = ['Climate change', 'Climate change']
        with patch('data.load_data', return_value=samples):
            app = atlas_app('pages/3_📊_Analysis.py').run(timeout=30)
        self.assertEqual(list(app.exception), [])
        texts = [item.value for item in app.info]
        self.assertEqual(len(texts), 5)
        self.assertIn('1 of 2 tracked species', texts[0])
        self.assertIn('50%', texts[0])
        self.assertIn('Test Region', texts[1])
        self.assertIn('2 of 2', texts[2])
        self.assertIn('2 of 2', texts[3])
        self.assertFalse(any(item.value.strip() == 'False' for item in app.markdown))
