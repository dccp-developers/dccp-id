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
        .front { background: #1a1a2e; color: #e0e0e0; display: flex; flex-direction: column; align-items: center; padding: 12px 14px; border-radius: 8px; }
        .school-name { font-size: 7px; font-weight: bold; letter-spacing: 3px; text-transform: uppercase; color: #e94560; }
        .card-title { font-size: 4px; color: #888; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }
        .photo-container { width: 56px; height: 56px; border-radius: 8px; overflow: hidden; border: 2px solid #e94560; background: #333; display: flex; align-items: center; justify-content: center; margin-bottom: 6px; }
        .photo-container img { width: 100%; height: 100%; object-fit: cover; }
        .photo-placeholder { font-size: 14px; color: #e94560; font-weight: bold; }
        .divider { width: 30px; height: 1px; background: linear-gradient(to right, #e94560, transparent); margin: 4px 0; }
        .student-name { font-size: 11px; font-weight: bold; color: #ffffff; text-align: center; }
        .student-course { font-size: 8px; color: #aaa; margin-top: 1px; text-align: center; }
        .student-id-number { font-size: 9px; font-weight: bold; color: #e94560; margin-top: 6px; letter-spacing: 1.5px; text-align: center; }
        .back { background: #1a1a2e; color: #e0e0e0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 18px 14px; border: 2px solid #16213e; border-radius: 8px; }
        .back-header { text-align: center; margin-bottom: 12px; width: 100%; border-bottom: 1px solid #e94560; padding-bottom: 6px; }
        .back-school-name { font-size: 7px; font-weight: bold; color: #e94560; letter-spacing: 2px; text-transform: uppercase; }
        .back-card-title { font-size: 4px; color: #888; letter-spacing: 1.5px; text-transform: uppercase; }
        .emergency-info { width: 100%; text-align: center; }
        .info-label { font-size: 6px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
        .info-value { font-size: 10px; font-weight: bold; color: #e0e0e0; margin-top: 2px; }
        .info-group { margin-bottom: 8px; }
        .barcode-area { margin-top: auto; text-align: center; width: 100%; padding-top: 8px; border-top: 1px solid #333; }
        .barcode-text { font-size: 7px; color: #666; font-family: 'Courier New', monospace; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="page front">
        <div class="school-name">DCCP</div>
        <div class="card-title">Student Identification Card</div>
        <div class="photo-container">
            @if($photoBase64)
                <img src="{{ $photoBase64 }}" alt="Student Photo">
            @else
                <div class="photo-placeholder">{{ strtoupper(substr($student->name, 0, 1)) }}</div>
            @endif
        </div>
        <div class="divider"></div>
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