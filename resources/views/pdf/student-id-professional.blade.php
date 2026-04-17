<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student ID - {{ $student->student_id_number }}</title>
    <style>
        @page { size: 2.125in 3.375in; margin: 0; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Georgia, serif; }
        .page { width: 2.125in; height: 3.375in; position: relative; overflow: hidden; page-break-after: always; }
        .front { background: #1b5e20; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 14px 12px; border-radius: 8px; }
        .school-name { font-size: 7px; font-weight: bold; letter-spacing: 3px; text-transform: uppercase; color: #a5d6a7; }
        .card-title { font-size: 4px; color: rgba(255,255,255,0.6); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }
        .separator { width: 28px; height: 2px; background: #a5d6a7; margin: 6px 0; border-radius: 1px; }
        .photo-container { width: 64px; height: 68px; border-radius: 4px; overflow: hidden; border: 2px solid #a5d6a7; background: #1b5e20; display: flex; align-items: center; justify-content: center; }
        .photo-container img { width: 100%; height: 100%; object-fit: cover; }
        .photo-placeholder { font-size: 18px; color: #a5d6a7; font-weight: bold; }
        .student-name { font-size: 11px; font-weight: bold; margin-top: 8px; text-align: center; }
        .student-course { font-size: 7px; color: #c8e6c9; margin-top: 2px; text-transform: uppercase; letter-spacing: 1px; text-align: center; }
        .student-id-number { font-size: 8px; font-weight: bold; background: #2e7d32; padding: 3px 12px; border-radius: 4px; display: inline-block; letter-spacing: 1.5px; margin-top: 6px; border: 1px solid #a5d6a7; }
        .back { background: #f1f8e9; color: #333; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px 14px; border: 2px solid #a5d6a7; border-radius: 8px; }
        .back-header { text-align: center; margin-bottom: 12px; width: 100%; border-bottom: 1px solid #a5d6a7; padding-bottom: 6px; }
        .back-school-name { font-size: 7px; font-weight: bold; color: #1b5e20; letter-spacing: 2px; text-transform: uppercase; }
        .back-card-title { font-size: 5px; color: #666; letter-spacing: 1.5px; text-transform: uppercase; }
        .emergency-info { width: 100%; text-align: center; }
        .info-label { font-size: 6px; color: #666; text-transform: uppercase; letter-spacing: 1px; }
        .info-value { font-size: 10px; font-weight: bold; color: #1b5e20; margin-top: 2px; }
        .info-group { margin-bottom: 8px; }
        .barcode-area { margin-top: auto; text-align: center; width: 100%; padding-top: 10px; border-top: 1px solid #a5d6a7; }
        .barcode-text { font-size: 7px; color: #888; font-family: 'Courier New', monospace; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="page front">
        <div class="school-name">DCCP</div>
        <div class="card-title">Student Identification Card</div>
        <div class="separator"></div>
        <div class="photo-container">
            @if($photoBase64)
                <img src="{{ $photoBase64 }}" alt="Student Photo">
            @else
                <div class="photo-placeholder">{{ strtoupper(substr($student->name, 0, 1)) }}</div>
            @endif
        </div>
        <div class="student-name">{{ strtoupper($student->name) }}</div>
        <div class="student-course">{{ strtoupper($student->course) }}</div>
        <div class="student-id-number">{{ $student->student_id_number }}</div>
    </div>
    <div class="page back">
        <div class="back-header">
            <div class="back-school-name">DCCP</div>
            <div class="back-card-title">Emergency Contact</div>
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