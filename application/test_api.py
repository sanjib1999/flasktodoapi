import unittest
import requests


class TestApi(unittest.TestCase):
    URL="http://127.0.0.1:5000/todolist"

    data={
        "Name":"testing",
        "Description":"testing postfunctionlity",
        "Type": "Good",
        "Age":5
    }

    expected_result={
        "Age": 7, 
        "Checked": False, 
        "Date": "2022-05-12T19:04:33.772607", 
        "Description": "todo 2 desc", 
        "Name": "todo 2", 
        "Type": "Average", 
        "id": 2
    }

    update_data={
        "Name":"updated",
        "Description":"updated post functionlity",
        "Type":"Average",
        "Age":4,
        "Checked":True
    }

    def test_1_get_all_todos(self):
        resp=requests.get(self.URL)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(len(resp.json()),3)
        print("Test 1 completed")
    def test_2_post_todo(self):
        resp=requests.post(self.URL, json=self.data )
        self.assertEqual(resp.status_code, 200)
        #self.assertDictEqual(resp.dict(),self.data)
        print("Test 2 completed")
    
    def test_3_get_specific_todo(self):
        resp=requests.get(self.URL+'/2')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(),self.expected_result)
        print("Test 3 completed")
    def test_4_delete(self):
        resp=requests.delete(self.URL+'/4')
        self.assertEqual(resp.status_code,200)
        print('test 4 completed')

    def test_5_update_data(self):
        resp=requests.put(self.URL+'/4', json=self.update_data)
        self.assertEqual(resp.json()['Name'],self.update_data['Name']) 
        self.assertEqual(resp.json()['Description'],self.update_data['Description'])
        self.assertEqual(resp.json()['Type'],self.update_data['Type'])
        self.assertEqual(resp.json()['Age'],self.update_data['Age'])
        self.assertEqual(resp.json()['Checked'],self.update_data['Checked'])
        print("test 5 completed")

if __name__=="__main__":
    tester=TestApi()
    tester.test_1_get_all_todos()
    #tester.test_2_post_todo()
    tester.test_3_get_specific_todo()
    tester.test_4_delete()
    #tester.test_5_update_data()