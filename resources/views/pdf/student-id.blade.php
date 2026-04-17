<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student ID - {{ $student->student_id_number }}</title>
    <style>
        @page {
            size: 3.375in 2.125in;
            margin: 0;
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, Helvetica, sans-serif;
            -webkit-font-smoothing: antialiased;
        }
        .page {
            width: 3.375in;
            height: 2.125in;
            position: relative;
            overflow: hidden;
            page-break-after: always;
        }
        .front {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 50%, #1e3a5f 100%);
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 8px 12px;
            border: 2px solid #1e3a5f;
            border-radius: 8px;
        }
        .header {
            text-align: center;
            margin-bottom: 4px;
            width: 100%;
        }
        .school-name {
            font-size: 7px;
            font-weight: bold;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .card-title {
            font-size: 5px;
            opacity: 0.85;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .photo-container {
            width: 55px;
            height: 55px;
            border-radius: 4px;
            overflow: hidden;
            border: 1.5px solid rgba(255,255,255,0.6);
            background: #ccc;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 3px 0;
            flex-shrink: 0;
        }
        .photo-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .photo-placeholder {
            font-size: 6px;
            color: #666;
            text-align: center;
        }
        .student-info {
            text-align: center;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .student-name {
            font-size: 8px;
            font-weight: bold;
            margin-bottom: 1px;
        }
        .student-course {
            font-size: 6px;
            opacity: 0.9;
            margin-bottom: 1px;
        }
        .student-id-number {
            font-size: 7px;
            font-weight: bold;
            background: rgba(255,255,255,0.15);
            padding: 1px 8px;
            border-radius: 3px;
            display: inline-block;
            letter-spacing: 1px;
        }
        .back {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
        }
        .back-header {
            text-align: center;
            margin-bottom: 8px;
            width: 100%;
            border-bottom: 1px solid #adb5bd;
            padding-bottom: 4px;
        }
        .back-school-name {
            font-size: 6px;
            font-weight: bold;
            color: #1e3a5f;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .back-card-title {
            font-size: 4.5px;
            color: #666;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .emergency-info {
            width: 100%;
            text-align: center;
        }
        .info-label {
            font-size: 5px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 1px;
        }
        .info-value {
            font-size: 7px;
            font-weight: bold;
            color: #333;
            margin-bottom: 6px;
        }
        .barcode-area {
            margin-top: auto;
            text-align: center;
            width: 100%;
            padding-top: 6px;
            border-top: 1px solid #adb5bd;
        }
        .barcode-text {
            font-size: 6px;
            color: #888;
            font-family: 'Courier New', monospace;
            letter-spacing: 2px;
        }
    </style>
</head>
<body>
    <div class="page front">
        <div class="header">
            <div class="school-name">D CCP</div>
            <div class="card-title">Student Identification Card</div>
        </div>
        <div class="photo-container">
            @if($photoBase64)
                <img src="{{ $photoBase64 }}" alt="Student Photo">
            @else
                <div class="photo-placeholder">No Photo</div>
            @endif
        </div>
        <div class="student-info">
            <div class="student-name">{{ strtoupper($student->name) }}</div>
            <div class="student-course">{{ strtoupper($student->course) }}</div>
            <div class="student-id-number">{{ $student->student_id_number }}</div>
        </div>
    </div>

    <div class="page back">
        <div class="back-header">
            <div class="back-school-name">DCCP</div>
            <div class="back-card-title">Emergency Contact Information</div>
        </div>
        <div class="emergency-info">
            <div class="info-label">Contact Number</div>
            <div class="info-value">{{ $student->contact_number }}</div>

            <div class="info-label">Guardian / Contact Person</div>
            <div class="info-value">{{ $student->guardian_contact_person }}</div>
        </div>
        <div class="barcode-area">
            <div class="barcode-text">ID: {{ $student->student_id_number }}</div>
        </div>
    </div>
</body>
</html>