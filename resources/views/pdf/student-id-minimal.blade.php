<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student ID - {{ $student->student_id_number }}</title>
    <style>
        @page { size: 2.125in 3.375in; margin: 0; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Helvetica Neue', Arial, sans-serif; }
        .page { width: 2.125in; height: 3.375in; position: relative; overflow: hidden; page-break-after: always; }
        .front { background: #ffffff; color: #333; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 16px 14px; border: 1px solid #ddd; border-radius: 10px; }
        .school-name { font-size: 7px; font-weight: 600; color: #999; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 8px; }
        .photo-container { width: 56px; height: 56px; border-radius: 50%; overflow: hidden; border: 2px solid #eee; background: #f5f5f5; display: flex; align-items: center; justify-content: center; margin-bottom: 8px; }
        .photo-container img { width: 100%; height: 100%; object-fit: cover; }
        .photo-placeholder { font-size: 16px; color: #ccc; font-weight: bold; }
        .student-name { font-size: 12px; font-weight: 700; color: #222; text-align: center; }
        .student-course { font-size: 8px; color: #888; margin-top: 2px; text-transform: uppercase; letter-spacing: 1px; }
        .student-id-number { font-size: 9px; color: #555; margin-top: 8px; font-family: 'Courier New', monospace; letter-spacing: 2px; padding: 2px 14px; border: 1px solid #ddd; border-radius: 20px; }
        .back { background: #fafafa; color: #333; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px 14px; border: 1px solid #ddd; border-radius: 10px; }
        .back-header { text-align: center; margin-bottom: 14px; padding-bottom: 8px; border-bottom: 1px solid #eee; width: 100%; }
        .back-school-name { font-size: 7px; font-weight: 600; color: #999; letter-spacing: 4px; text-transform: uppercase; }
        .back-card-title { font-size: 5px; color: #bbb; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 2px; }
        .emergency-info { width: 100%; text-align: center; }
        .info-label { font-size: 6px; color: #bbb; text-transform: uppercase; letter-spacing: 1.5px; }
        .info-value { font-size: 10px; font-weight: 600; color: #333; margin-top: 2px; }
        .info-group { margin-bottom: 10px; }
        .barcode-area { margin-top: auto; text-align: center; width: 100%; padding-top: 10px; border-top: 1px solid #eee; }
        .barcode-text { font-size: 7px; color: #ccc; font-family: 'Courier New', monospace; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="page front">
        <div class="school-name">DCCP</div>
        <div class="photo-container">
            @if($photoBase64)
                <img src="{{ $photoBase64 }}" alt="Student Photo">
            @else
                <div class="photo-placeholder">{{ strtoupper(substr($student->name, 0, 1)) }}</div>
            @endif
        </div>
        <div class="student-name">{{ $student->name }}</div>
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
            <div class="barcode-text">{{ $student->student_id_number }}</div>
        </div>
    </div>
</body>
</html>