<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student ID - {{ $student->student_id_number }}</title>
    <style>
        @page { size: 2.125in 3.375in; margin: 0; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, Helvetica, sans-serif; }
        .page { width: 2.125in; height: 3.375in; position: relative; overflow: hidden; page-break-after: always; border-radius: 8px; }
        .element { position: absolute; }
    </style>
</head>
<body>
    @php
        $config = $config ?? [];
        $front = $config['front'] ?? [];
        $back = $config['back'] ?? [];

        $placeholderMap = [
            '{{student.name}}' => strtoupper($student->name),
            '{{student.course}}' => strtoupper($student->course),
            '{{student.student_id_number}}' => $student->student_id_number,
            '{{student.contact_number}}' => $student->contact_number,
            '{{student.guardian_contact_person}}' => $student->guardian_contact_person,
            '{{school_name}}' => 'DCCP',
        ];

        function renderBackground($side) {
            $bg = $side['background'] ?? [];
            $type = $bg['type'] ?? 'solid';

            if ($type === 'gradient') {
                $start = $bg['gradientStart'] ?? '#667eea';
                $end = $bg['gradientEnd'] ?? '#764ba2';
                $angle = $bg['gradientAngle'] ?? '135';
                return "background: linear-gradient({$angle}deg, {$start}, {$end});";
            }

            if ($type === 'image' && !empty($bg['imageBase64'])) {
                return "background-image: url('{$bg['imageBase64']}'); background-size: cover; background-position: center;";
            }

            $color = $bg['solidColor'] ?? '#1e3a5f';
            return "background-color: {$color};";
        }

        function renderElement($el, $placeholderMap, $photoBase64) {
            $type = $el['type'] ?? 'text';
            $x = ($el['x'] ?? 50) . '%';
            $y = ($el['y'] ?? 50) . '%';
            $fontSize = ($el['fontSize'] ?? 10) . 'pt';
            $fontWeight = ($el['fontWeight'] ?? 'normal') === 'bold' ? 'bold' : 'normal';
            $color = $el['color'] ?? '#ffffff';
            $textAlign = $el['textAlign'] ?? 'center';
            $textTransform = $el['textTransform'] ?? 'none';

            if ($type === 'photo') {
                $w = ($el['width'] ?? 20) . '%';
                $h = ($el['height'] ?? 25) . '%';
                $br = ($el['borderRadius'] ?? 6) . 'px';
                $transform = 'translate(-50%, -50%)';
                if ($photoBase64) {
                    return "<div class=\"element\" style=\"left: {$x}; top: {$y}; width: {$w}; height: {$h}; transform: {$transform}; border-radius: {$br}; overflow: hidden; border: 2px solid rgba(255,255,255,0.5);\"><img src=\"{$photoBase64}\" style=\"width: 100%; height: 100%; object-fit: cover;\"></div>";
                }
                return "<div class=\"element\" style=\"left: {$x}; top: {$y}; width: {$w}; height: {$h}; transform: {$transform}; border-radius: {$br}; background: rgba(128,128,128,0.3); display: flex; align-items: center; justify-content: center; font-size: 14pt; color: rgba(255,255,255,0.6);\">" . strtoupper(substr($student->name ?? 'S', 0, 1)) . "</div>";
            }

            $content = $el['content'] ?? '';
            $content = str_replace(array_keys($placeholderMap), array_values($placeholderMap), $content);

            $transform = 'translate(-50%, -50%)';

            return "<div class=\"element\" style=\"left: {$x}; top: {$y}; transform: {$transform}; font-size: {$fontSize}; font-weight: {$fontWeight}; color: {$color}; text-align: {$textAlign}; text-transform: {$textTransform}; white-space: nowrap;\">{$content}</div>";
        }
    @endphp

    {{-- FRONT --}}
    <div class="page" style="{{ renderBackground($front) }}">
        @foreach(($front['elements'] ?? []) as $element)
            {!! renderElement($element, $placeholderMap, $photoBase64) !!}
        @endforeach
    </div>

    {{-- BACK --}}
    <div class="page" style="{{ renderBackground($back) }}">
        @foreach(($back['elements'] ?? []) as $element)
            {!! renderElement($element, $placeholderMap, $photoBase64) !!}
        @endforeach
    </div>
</body>
</html>