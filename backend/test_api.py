import urllib.request
import json
import sys

def test_api():
    base = 'http://127.0.0.1:8000'
    
    # 1. Health
    with urllib.request.urlopen(f'{base}/api/health') as r:
        health = json.loads(r.read().decode('utf-8'))
        print('1. Health Check:', health['status'], '| Modules:', list(health['modules'].keys()))
        assert health['status'] == 'healthy'
        
    # 2. Languages
    with urllib.request.urlopen(f'{base}/api/languages') as r:
        langs = json.loads(r.read().decode('utf-8'))
        print('2. Languages:', [l['code'] for l in langs])
        assert len(langs) == 3

    # 3. Emergency Triage (Tamil)
    req_data = json.dumps({
        'symptoms_text': 'நெஞ்சு வலி மற்றும் மூச்சுத்திணறல்',
        'language': 'ta',
        'age_group': 'adult',
        'duration': '< 24 hours',
        'save_to_history': True
    }).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/triage', data=req_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode('utf-8'))
        print('3. Tamil Triage Category:', res['urgency_category'], '| Title:', res['urgency_title'])
        assert res['urgency_category'] == 'EMERGENCY'
        assert res['assessment_id'] is not None
        assert 'அவசர' in res['urgency_title'] or 'Emergency' in res['urgency_title']
        saved_id = res['assessment_id']

    # 4. Text-extracted Duration: Fever 5 days (Tamil) -> URGENT
    req_data = json.dumps({
        'symptoms_text': 'காய்ச்சல் 5 நாள் மற்றும் கடுமையான உடல் சோர்வு',
        'language': 'ta',
        'age_group': 'adult',
        'save_to_history': False
    }).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/triage', data=req_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode('utf-8'))
        print('4. Extracted Duration Triage:', res['urgency_category'], '| Title:', res['urgency_title'])
        assert res['urgency_category'] == 'URGENT'

    # 5. Animal Bite (Rabies Risk) -> EMERGENCY
    req_data = json.dumps({
        'symptoms_text': 'நாய்க்கடி காலில் ரத்தம் வருகிறது',
        'language': 'ta',
        'age_group': 'child'
    }).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/triage', data=req_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode('utf-8'))
        print('5. Animal Bite Triage:', res['urgency_category'])
        assert res['urgency_category'] == 'EMERGENCY'

    # 6. Obstetric Emergency -> EMERGENCY
    req_data = json.dumps({
        'symptoms_text': 'गर्भावस्था में तेज पेट दर्द और अत्यधिक रक्तस्राव',
        'language': 'hi',
        'age_group': 'adult'
    }).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/triage', data=req_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode('utf-8'))
        print('6. Obstetric Triage:', res['urgency_category'])
        assert res['urgency_category'] == 'EMERGENCY'

    # 7. Routine Triage (Hindi)
    req_data = json.dumps({
        'symptoms_text': 'हल्की खांसी और जुकाम दो दिन से',
        'language': 'hi',
        'age_group': 'adult',
        'duration': '1-3 days'
    }).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/triage', data=req_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode('utf-8'))
        print('7. Hindi Routine Triage Category:', res['urgency_category'])
        assert res['urgency_category'] == 'ROUTINE'

    # 8. Structured Medical Summary with Pertinent Negatives
    summary_req = json.dumps({
        'symptoms_text': 'கடும் காய்ச்சல் 4 நாட்களாக',
        'translated_text': 'high fever for 4 days',
        'language': 'ta',
        'age_group': 'child',
        'duration': '4-7 days',
        'urgency_category': 'URGENT',
        'recognized_symptoms': ['high fever'],
        'recommended_action': 'Visit CHC within 24 hours',
        'recommended_facility_type': 'Community Health Centre (CHC)'
    }).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/summary', data=summary_req, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        s_res = json.loads(r.read().decode('utf-8'))
        print('8. Pertinent Negatives Detected:', len(s_res['pertinent_negatives']))
        assert len(s_res['pertinent_negatives']) > 0
        # Thermometer reading should be detected as missing
        assert any('temperature' in pn.lower() for pn in s_res['pertinent_negatives'])

    # 9. Facilities with GPS Distance
    with urllib.request.urlopen(f'{base}/api/facilities?lat=10.02&lon=78.33') as r:
        facs = json.loads(r.read().decode('utf-8'))
        closest = facs['facilities'][0]
        print(f"9. Facilities Near Melur: {facs['total']} found. Closest: {closest['name']} ({closest['distance_km']} km)")
        assert facs['total'] > 0
        assert closest['distance_km'] is not None

    # 10. Clinician Queue & Acknowledge
    with urllib.request.urlopen(f'{base}/api/clinician/queue') as r:
        queue = json.loads(r.read().decode('utf-8'))
        print(f"10. Clinician Queue: {len(queue)} cases | Top item urgency: {queue[0]['urgency_category']}")
        assert len(queue) > 0
        top_case_id = queue[0]['id']

    # Acknowledge case
    ack_data = json.dumps({
        'assessment_id': top_case_id,
        'clinician_name': 'Dr. Test Officer',
        'clinician_notes': 'Verified and triaged to emergency room.'
    }).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/clinician/acknowledge', data=ack_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        ack_res = json.loads(r.read().decode('utf-8'))
        print('10b. Clinician Acknowledged:', ack_res['status'])
        assert ack_res['status'] == 'success'

    # 11. Single assessment deletion
    req = urllib.request.Request(f'{base}/api/assessments/{saved_id}', method='DELETE')
    with urllib.request.urlopen(req) as r:
        del_res = json.loads(r.read().decode('utf-8'))
        print(f'11. Assessment {saved_id} Deleted:', del_res['status'])
        assert del_res['status'] == 'success'

    print('\n========================================')
    print('ALL 11 BACKEND API TEST SUITES PASSED!')
    print('========================================')

if __name__ == '__main__':
    test_api()
