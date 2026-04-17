<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student ID - {{ $student->student_id_number }}</title>
    <style>
        @page { size: 2.125in 3.375in; margin: 0; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, Helvetica, sans-serif; }
        .page { width: 2.125in; height: 3.375in; position: relative; overflow: hidden; page-break-after: always; }
        .front { background: linear-gradient(180deg, #667eea 0%, #764ba2 100%); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 16px 14px; border-radius: 10px; }
        .school-name { font-size: 8px; font-weight: bold; letter-spacing: 2px; text-transform: uppercase; }
        .card-title { font-size: 5px; opacity: 0.7; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 2px; }
        .accent-bar { width: 55%; height: 2px; background: rgba(255,255,255,0.4); border-radius: 2px; margin: 8px 0; }
        .photo-container { width: 56px; height: 56px; border-radius: 8px; overflow: hidden; border: 2px solid rgba(255,255,255,0.5); background: rgba(255,255,255,0.15); display: flex; align-items: center; justify-content: center; margin-bottom: 8px; }
        .photo-container img { width: 100%; height: 100%; object-fit: cover; }
        .photo-placeholder { font-size: 14px; color: rgba(255,255,255,0.6); font-weight: bold; }
        .student-name { font-size: 11px; font-weight: bold; text-align: center; }
        .student-course { font-size: 7px; opacity: 0.9; margin-top: 2px; text-align: center; }
        .id-badge { font-size: 8px; font-weight: bold; background: rgba(255,255,255,0.25); padding: 3px 14px; border-radius: 12px; display: inline-block; letter-spacing: 1.5px; margin-top: 8px; }
        .back { background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 100%); color: #444; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px 14px; border-radius: 10px; }
        .back-header { text-align: center; margin-bottom: 12px; width: 80%; border-bottom: 2px solid #764ba2; padding-bottom: 6px; }
        .back-school-name { font-size: 7px; font-weight: bold; color: #764ba2; letter-spacing: 2px; text-transform: uppercase; }
        .back-card-title { font-size: 5px; color: #888; letter-spacing: 1.5px; text-transform: uppercase; }
        .emergency-info { width: 100%; text-align: center; }
        .info-label { font-size: 6px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
        .info-value { font-size: 10px; font-weight: bold; color: #333; margin-top: 2px; }
        .info-group { margin-bottom: 8px; }
        .barcode-area { margin-top: auto; text-align: center; width: 100%; padding-top: 10px; border-top: 1px solid #b0b0b0; }
        .barcode-text { font-size: 7px; color: #999; font-family: 'Courier New', monospace; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="page front">
        <div class="school-name">DCCP</div>
        <div class="card-title">Student Identification Card</div>
        <div class="accent-bar"></div>
        <div class="photo-container">
            @if($photoBase64)
                <img src="{{ $photoBase64 }}" alt="Student Photo">
            @else
                <div class="photo-placeholder">{{ strtoupper(substr($student->name, 0, 1)) }}</div>
            @endif
        </div>
        <div class="student-name">{{ strtoupper($student->name) }}</div>
        <div class="student-course">{{ strtoupper($student->course) }}</div>
        <div class="id-badge">{{ $student->student_id_number }}</div>
    </div>
    <div class="page back">
        <div class="back-header">
            <div class="back-school-name">DCCP</div>
            <div class="back-card-title">Emergency Contact Information</div>
        </div>
        <div class="emergency-info">
            <div class="info-group">
                <div class="info-label">Contact Number</div>
                <div class="info-value">{{ $student->contact_number }}</div>
            </div>
            <div class="info-group">
                <div class="info-label">Guardian / Contact Person</div>
                <div class="info-value">{{ $student->guardian_contact_person }}</div>
            </div>
        </div>
        <div class="barcode-area">
            <div class="barcode-text">ID: {{ $student->student_id_number }}</div>
        </div>
    </div>
</body>
</html>