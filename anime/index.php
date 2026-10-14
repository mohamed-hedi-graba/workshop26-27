<?php

function set_character_cookie($char) {
    $val = base64_encode(serialize($char));
    setcookie('character', $val, time() + 3600, '/');
}

function get_character_from_cookie() {
    if (!isset($_COOKIE['character'])) return null;
    $raw = base64_decode($_COOKIE['character'], true);
    if ($raw === false) return null;
    $obj = @unserialize($raw);
    if (!is_array($obj) || !isset($obj['name'], $obj['anime_name'], $obj['img'], $obj['strength'], $obj['health'])) {
        return null;
    }
    return $obj;
}

function set_saitama_cookie($saitama) {
    $val = base64_encode(serialize($saitama));
    setcookie('saitama', $val, time() + 3600, '/');
}

function get_saitama_from_cookie() {
    if (!isset($_COOKIE['saitama'])) return null;
    $raw = base64_decode($_COOKIE['saitama'], true);
    if ($raw === false) return null;
    $obj = @unserialize($raw);
    if (!is_array($obj) || !isset($obj['name'], $obj['anime_name'], $obj['img'], $obj['strength'], $obj['health'])) {
        return null;
    }
    return $obj;
}

// Static roster (12 characters) with placeholder images
$roster = [
    ["name" => "Naruto Uzumaki", "anime_name" => "Naruto", "img" => "https://s.cafebazaar.ir/images/icons/com.bandainamcoent.ninjavoltage_app-1ab0a9af-c962-47ad-9eb1-d6eaac165b20_512x512.png?x-img=v1/resize,h_256,w_256,lossless_false/optimize", "strength" => 85, "health" => 180],
    ["name" => "Goku", "anime_name" => "Dragon Ball", "img" => "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTi6BwgV5sihY4QTe1OB7v9Me7a-jTpOPYtvA&s", "strength" => 100, "health" => 200],
    ["name" => "Ichigo Kurosaki", "anime_name" => "Bleach", "img" => "https://images.steamusercontent.com/ugc/1829032543099085155/33F3D356611217F2108EB90CB47DA864027A4B9C/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false", "strength" => 88, "health" => 170],
    ["name" => "Kenshiro", "anime_name" => "Fist of the North Star", "img" => "https://files.shapes.inc/api/files/avatar_d141b5a5-c7e4-4ff9-a5dc-40f3f509b8a7.png", "strength" => 92, "health" => 190],
    ["name" => "Alucard", "anime_name" => "Hellsing", "img" => "https://singifyai.fineshare.com/song-ai/covers/alucard-hellsing.webp", "strength" => 80, "health" => 160],
    ["name" => "Jotaro Kujo", "anime_name" => "JoJo", "img" => "https://i.pinimg.com/736x/77/c9/a9/77c9a9da684796628c5f66715ed5266b.jpg", "strength" => 90, "health" => 175],
    ["name" => "Dio Brando", "anime_name" => "JoJo", "img" => "https://files.shapes.inc/api/files/avatar_47fe6ff2-43e5-47eb-9575-b205fb61996f.png", "strength" => 95, "health" => 165],
    ["name" => "Edward Elric", "anime_name" => "FMA", "img" => "https://files.shapes.inc/api/files/avatar_ac474ff8-e3d4-41a5-9b9a-7fbc02ad71c3.png", "strength" => 65, "health" => 140],
    ["name" => "Sailor Moon", "anime_name" => "Sailor Moon", "img" => "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQE20UbLIGXcxxU1RmaeAIXoxAdmtBdE1bQSA&s", "strength" => 55, "health" => 130],
    ["name" => "Luffy", "anime_name" => "One Piece", "img" => "https://b.thumbs.redditmedia.com/X4VDgVKqsiTnA22tAJQ72MHJQs7Sd7hsFaBBqLqIqcY.png", "strength" => 93, "health" => 185],
    ["name" => "Light Yagami", "anime_name" => "Death Note", "img" => "https://fish.audio/_next/image/?url=https%3A%2F%2Fpublic-platform.r2.fish.audio%2Fcoverimage%2Fb38c007780a24aaca5e16b2e40b223b9&w=256&q=75", "strength" => 45, "health" => 120],
    ["name" => "Mikasa Ackerman", "anime_name" => "Attack on Titan", "img" => "https://i.pinimg.com/474x/94/73/aa/9473aa51fb6cdb4b96414e9ed2660a2c.jpg", "strength" => 78, "health" => 155],
];

// Saitama default
$default_saitama = [
    'name' => 'Saitama',
    'anime_name' => 'One Punch Man',
    'strength' => 500,
    'health' => 500,
    'img' => 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRt-EW7-A1jWkL2g-Dn4yrFSeuQKuEu4qpTww&s'
];

// Routing-ish: choose, fight, attack, reset
$action = $_GET['action'] ?? null;
$show_popup = false; // Initialize popup flag
$messages = [];

// Reset game
if ($action === 'reset') {
    setcookie('character', '', time() - 3600, '/');
    setcookie('saitama', '', time() - 3600, '/');
    header('Location: /');
    exit;
}

// Player chooses a character
if ($action === 'choose' && isset($_GET['id'])) {
    $id = (int) $_GET['id'];
    if (!isset($roster[$id])) {
        header('Location: /');
        exit;
    }
    $base = $roster[$id];
    set_character_cookie($base);
    set_saitama_cookie($default_saitama);
    header('Location: ?action=fight');
    exit;
}

// Fight mechanics
if ($action === 'attack') {
    $player = get_character_from_cookie();
    $saitama = get_saitama_from_cookie();
    if (!$player || !$saitama) {
        $messages[] = "No game in progress. Please choose a character first.";
        header('Location: /');
        exit;
    } else {
        // Player attacks first
        $saitama['health'] -= (int)$player['strength'];
        $messages[] = "{$player['name']} hits Saitama for {$player['strength']} damage!";

        if ($saitama['health'] <= 0) {
            $messages[] = "Saitama falls! You win!";
            $messages[] = getenv('FLAG');
            set_saitama_cookie($saitama);
            // Do not clear cookies; show final state
        } else {
            // Saitama strikes back
            $player['health'] -= (int)$saitama['strength'];
            $messages[] = "Saitama punches back for {$saitama['strength']} damage!";

            if ($player['health'] <= 0) {
                $messages[] = "{$player['name']} has fallen. Game over.";
                $show_popup = true;
                set_character_cookie($player);
                // Do not clear cookies; show final state
            } else {
                set_character_cookie($player);
                set_saitama_cookie($saitama);
                // Redirect to fight to prevent refresh re-attack
                header('Location: ?action=fight');
                exit;
            }
        }
    }
    // If we reach here, it's game over; fall through to display fight with messages and popup
}

// If visiting fight screen, ensure valid game state
if ($action === 'fight') {
    $player = get_character_from_cookie();
    $saitama = get_saitama_from_cookie();
    if (!$player || !$saitama) {
        header('Location: /');
        exit;
    }
    if ($player['health'] <= 0) {
        $show_popup = true;
    }
}

// Helper to display health bars
function render_health_bar($current, $max = 500) {
    $pct = max(0, min(100, round(($current / $max) * 100)));
    return "<div class=\"hpbar\"><div class=\"hpfill\" style=\"width: {$pct}%\"></div></div>";
}

?><!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Anime Battle: Saitama vs You</title>
    <style>
        body { background: linear-gradient(120deg,#0f172a,#0b1b2b); color: #e6eef8; font-family: Arial, Helvetica, sans-serif; margin: 0; padding: 20px; }
        h1 { font-family: 'Trebuchet MS', sans-serif; letter-spacing: 1px; }
        .container { max-width: 1000px; margin: 0 auto; }
        .roster { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-top: 20px; }
        .card { background: rgba(255,255,255,0.04); padding: 10px; border-radius: 12px; text-align:center; box-shadow: 0 6px 18px rgba(0,0,0,0.5); }
        img { max-width: 100%; border-radius: 8px; }
        .btn { display:inline-block; padding: 8px 12px; margin-top:8px; background:#ffcc00; color:#111; border-radius:8px; font-weight:bold; text-decoration:none; }
        .topbar { display:flex; justify-content:space-between; align-items:center; }
        .battle { display:flex; gap:20px; margin-top:20px; align-items:flex-start; }
        .col { flex:1; background: rgba(255,255,255,0.03); padding: 12px; border-radius: 10px; }
        .hpbar { width:100%; height:14px; background: rgba(255,255,255,0.06); border-radius: 8px; overflow:hidden; }
        .hpfill { height:100%; background: linear-gradient(90deg,#16a34a,#22c55e); }
        .messages { margin-top:12px; }
        .message { background: rgba(255,255,255,0.03); padding:8px; border-radius:6px; margin-bottom:6px; }
        .actions { margin-top:12px; }
        .small { font-size:0.9rem; color:#cbd5e1; }
        footer { margin-top:30px; color:#9fb2d3; font-size:0.85rem; }
        /* Modal styles */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 1000; justify-content: center; align-items: center; }
        .modal-content { background: #1e293b; padding: 20px; border-radius: 12px; text-align: center; max-width: 400px; width: 90%; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
        .modal-content h2 { margin: 0 0 10px; color: #ff4444; }
        .modal-content p { margin: 0 0 20px; color: #e6eef8; }
        .modal-content .btn { background: #ff4444; color: #fff; }
    </style>
</head>
<body>
<div class="container">
    <!-- Modal HTML -->
    <div id="gameOverModal" class="modal">
        <div class="modal-content">
            <h2>Game Over!</h2>
            <p>You have been defeated by Saitama. Try again?</p>
            <a class="btn" href="?action=reset">Reset Game</a>
        </div>
    </div>

    <div class="topbar">
        <div>
            <h1>Anime Battle</h1>
            <div class="small">Choose a character and face <strong>Saitama</strong> — powerful but beatable if luck is on your side.</div>
        </div>
        <div>
            <a class="btn" href="?action=reset">Reset Game</a>
        </div>
    </div>

<?php if (!isset($_COOKIE['character']) || !get_character_from_cookie()): ?>
    <h2>Choose your character</h2>
    <div class="roster">
        <?php foreach ($roster as $i => $c): ?>
            <div class="card">
                <img src="<?= htmlspecialchars($c['img']) ?>" alt="<?= htmlspecialchars($c['name']) ?>">
                <h3><?= htmlspecialchars($c['name']) ?></h3>
                <div class="small"><?= htmlspecialchars($c['anime_name']) ?></div>
                <a class="btn" href="?action=choose&id=<?= $i ?>">Choose</a>
            </div>
        <?php endforeach; ?>
    </div>
<?php else: ?>
    <?php
        // Reload after potential updates in attack
        $player = get_character_from_cookie();
        $saitama = get_saitama_from_cookie() ?: $default_saitama;
    ?>
    <h2>Battle Field</h2>
    <div class="battle">
        <div class="col">
            <h3><?= htmlspecialchars($player['name']) ?> <span class="small">(<?= htmlspecialchars($player['anime_name']) ?>)</span></h3>
            <img src="<?= htmlspecialchars($player['img']) ?>" alt="player">
            <p class="small">Strength: <?= (int)$player['strength'] ?> | Health: <?= max(0, (int)$player['health']) ?></p>
            <?= render_health_bar(max(0, (int)$player['health']), 200) ?>
        </div>

        <div class="col">
            <h3><?= htmlspecialchars($saitama['name']) ?> <span class="small">(<?= htmlspecialchars($saitama['anime_name']) ?>)</span></h3>
            <img src="<?= htmlspecialchars($saitama['img']) ?>" alt="saitama">
            <p class="small">Strength: <?= (int)$saitama['strength'] ?> | Health: <?= max(0, (int)$saitama['health']) ?></p>
            <?= render_health_bar(max(0, (int)$saitama['health']), 500) ?>
        </div>
    </div>

    <div class="messages">
        <?php foreach ($messages as $m): ?>
            <div class="message"><?= htmlspecialchars($m) ?></div>
        <?php endforeach; ?>
    </div>

    <div class="actions">
        <?php
            $game_over = ($player['health'] <= 0 || $saitama['health'] <= 0);
        ?>
        <?php if (!$game_over): ?>
            <a class="btn" href="?action=attack">Attack</a>
        <?php else: ?>
            <div class="message">Game over. <a href="?action=reset">Reset Game</a> to start again.</div>
        <?php endif; ?>
    </div>
<?php endif; ?>
</div>

<script>
    function showModal() {
        document.getElementById('gameOverModal').style.display = 'flex';
    }
    <?php if ($show_popup): ?>
        window.onload = showModal;
    <?php endif; ?>
</script>
</body>
</html>