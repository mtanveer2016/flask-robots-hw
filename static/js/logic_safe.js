// ============================================
// API CONFIGURATION
// ============================================
const ROBOT_API_BASE = 'http://10.243.53.235:5005';
const ROBOT_COUNT = 10;

let activeTimeouts = {};
let selectedRobotIndex = 0;
let isDancing = false;

function sendCommand(robotId, command) {
    console.log(`[CMD] Robot ${robotId}: ${command}`);
    
    $.get(`${ROBOT_API_BASE}/move/${robotId}/${command}`, function(data) {
        console.log(`[OK] Robot ${robotId}: ${command}`, data);
        showRobotFeedback(robotId, command);
    }).fail(function(err) {
        console.error(`[ERR] Robot ${robotId}:`, err);
        showRobotFeedback(robotId, 'error');
    });
}

function emergencyStop() {
    console.log("🚨 EMERGENCY STOP!");
    $.get(`${ROBOT_API_BASE}/stop/all`, function(data) {
        console.log("✅ Emergency stop activated");
        showGlobalNotification("🚨 EMERGENCY STOP! 🚨", "#dc2626", 3000);
        // Stop any ongoing dance
        if (window.danceInterval) clearInterval(window.danceInterval);
    });
}

function stopDance() {
    console.log("🛑 Stopping dance...");
    $.get(`${ROBOT_API_BASE}/dance/stop`, function(data) {
        console.log("✅ Dance stopped");
        showGlobalNotification("🛑 Dance stopped", "#f39c12", 1500);
    });
}

function startDance() {
    console.log("💃 Starting dance...");
    $.get(`${ROBOT_API_BASE}/dance`, function(data) {
        console.log("✅ Dance started");
        showGlobalNotification("💃 Dancing! Press STOP to cancel 🕺", "#e74c3c", 2000);
    }).fail(function(err) {
        console.error("Dance error:", err);
        showGlobalNotification("Dance already in progress", "#f39c12", 1500);
    });
}

function showRobotFeedback(robotId, command, duration = 800) {
    const card = $(`.robot-card[data-robot-idx="${robotId}"]`);
    if (!card.length) return;
    
    let feedbackText = '';
    let emoji = '';
    switch(command) {
        case 'forward': feedbackText = 'FORWARD'; emoji = '⬆️'; break;
        case 'backward': feedbackText = 'BACKWARD'; emoji = '⬇️'; break;
        case 'left': feedbackText = 'LEFT'; emoji = '⬅️'; break;
        case 'right': feedbackText = 'RIGHT'; emoji = '➡️'; break;
        case 'stop': feedbackText = 'STOP'; emoji = '🛑'; break;
        case 'error': feedbackText = 'ERROR'; emoji = '❌'; break;
        default: feedbackText = command; emoji = '🎵';
    }
    
    card.find('.command-feedback').remove();
    const feedback = $(`<div class="command-feedback">${emoji} ${feedbackText}</div>`);
    feedback.css({
        'position': 'absolute',
        'top': '50%',
        'left': '50%',
        'transform': 'translate(-50%, -50%)',
        'background': 'rgba(0,0,0,0.85)',
        'color': 'white',
        'padding': '4px 10px',
        'border-radius': '20px',
        'font-size': '12px',
        'font-weight': 'bold',
        'z-index': '100',
        'white-space': 'nowrap',
        'pointer-events': 'none'
    });
    card.append(feedback);
    setTimeout(() => feedback.fadeOut(300, () => $(this).remove()), duration);
}

function setSelectedRobot(robotId) {
    if (robotId === undefined) return;
    selectedRobotIndex = robotId;
    $('.robot-card').removeClass('selected');
    $(`.robot-card[data-robot-idx="${robotId}"]`).addClass('selected');
    $('#selectedRobotId').text(`ROBOT ${parseInt(robotId) + 1}`);
}

function setupEventDelegation() {
    $(document).on('click', '[id^="select-"]', function() {
        const robotId = $(this).attr('id').split('-')[1];
        setSelectedRobot(parseInt(robotId));
    });
    
    $(document).on('click', '[id^="stop-"]', function() {
        const robotId = $(this).attr('id').split('-')[1];
        if (activeTimeouts[robotId]) clearTimeout(activeTimeouts[robotId]);
        sendCommand(parseInt(robotId), 'stop');
    });
    
    $(document).on('mousedown touchstart', '[id^="forward-"]', function(e) {
        e.preventDefault();
        const robotId = $(this).attr('id').split('-')[1];
        if (activeTimeouts[robotId]) clearTimeout(activeTimeouts[robotId]);
        sendCommand(parseInt(robotId), 'forward');
    });
    
    $(document).on('mouseup touchend', '[id^="forward-"]', function(e) {
        e.preventDefault();
        const robotId = $(this).attr('id').split('-')[1];
        activeTimeouts[robotId] = setTimeout(() => sendCommand(parseInt(robotId), 'stop'), 50);
    });
    
    $(document).on('mousedown touchstart', '[id^="backward-"]', function(e) {
        e.preventDefault();
        const robotId = $(this).attr('id').split('-')[1];
        if (activeTimeouts[robotId]) clearTimeout(activeTimeouts[robotId]);
        sendCommand(parseInt(robotId), 'backward');
    });
    
    $(document).on('mouseup touchend', '[id^="backward-"]', function(e) {
        e.preventDefault();
        const robotId = $(this).attr('id').split('-')[1];
        activeTimeouts[robotId] = setTimeout(() => sendCommand(parseInt(robotId), 'stop'), 50);
    });
    
    $(document).on('mousedown touchstart', '[id^="left-"]', function(e) {
        e.preventDefault();
        const robotId = $(this).attr('id').split('-')[1];
        if (activeTimeouts[robotId]) clearTimeout(activeTimeouts[robotId]);
        sendCommand(parseInt(robotId), 'left');
    });
    
    $(document).on('mouseup touchend', '[id^="left-"]', function(e) {
        e.preventDefault();
        const robotId = $(this).attr('id').split('-')[1];
        activeTimeouts[robotId] = setTimeout(() => sendCommand(parseInt(robotId), 'stop'), 50);
    });
    
    $(document).on('mousedown touchstart', '[id^="right-"]', function(e) {
        e.preventDefault();
        const robotId = $(this).attr('id').split('-')[1];
        if (activeTimeouts[robotId]) clearTimeout(activeTimeouts[robotId]);
        sendCommand(parseInt(robotId), 'right');
    });
    
    $(document).on('mouseup touchend', '[id^="right-"]', function(e) {
        e.preventDefault();
        const robotId = $(this).attr('id').split('-')[1];
        activeTimeouts[robotId] = setTimeout(() => sendCommand(parseInt(robotId), 'stop'), 50);
    });
    
    $(document).on('click', '.robot-card', function(e) {
        if ($(e.target).is('button') || $(e.target).is('input')) return;
        const robotId = $(this).attr('data-robot-idx');
        if (robotId !== undefined) setSelectedRobot(parseInt(robotId));
    });
}

function controlAllRobots(command) {
    for (let i = 0; i < ROBOT_COUNT; i++) sendCommand(i, command);
}

function renderRobotsGrid() {
    const grid = $('#robotsGrid');
    grid.empty();
    for (let i = 0; i < ROBOT_COUNT; i++) {
        grid.append(`
            <div class="robot-card" data-robot-idx="${i}">
                <div class="robot-header">
                    <span class="robot-name">🤖 ROBOT ${i+1}</span>
                    <span class="robot-status"><span class="status-led"></span> active</span>
                </div>
                <div class="dpad">
                    <table style="margin:0 auto">
                        <tr><th></th><th><button id="forward-${i}">▲</button></th><th></th></tr>
                        <tr><td><button id="left-${i}">◀</button></td><td></td><td><button id="right-${i}">▶</button></td></tr>
                        <tr><td></td><td><button id="backward-${i}">▼</button></td><td></td></tr>
                    </table>
                </div>
                <div class="action-buttons">
                    <button id="select-${i}" class="select-btn">✅ Select</button>
                    <button id="stop-${i}" class="stop-btn">⏹️ Stop</button>
                </div>
            </div>
        `);
    }
    setSelectedRobot(0);
}

function showGlobalNotification(message, bgColor, duration) {
    let notification = $('#globalNotification');
    if (!notification.length) {
        notification = $(`<div id="globalNotification" style="position:fixed;bottom:30px;left:50%;transform:translateX(-50%);color:white;padding:12px 24px;border-radius:50px;z-index:9999;font-weight:bold;text-align:center;"></div>`);
        $('body').append(notification);
    }
    notification.css('background', bgColor).text(message).fadeIn(200);
    setTimeout(() => notification.fadeOut(500), duration);
}

$(document).ready(function() {
    console.log("🤖 Multi-Robot Control System Loaded");
    console.log(`🌐 API: ${ROBOT_API_BASE}`);
    
    renderRobotsGrid();
    setupEventDelegation();
    
    // Add emergency stop button to global panel
    $('.global-commands').prepend(`<button id="emergencyStop" style="background:#dc2626 !important; animation:pulse 1s infinite;">🚨 EMERGENCY STOP 🚨</button>`);
    $('.global-commands').append(`<button id="stopDance" style="background:#f39c12 !important;">🛑 Stop Dance</button>`);
    
    $('#emergencyStop').on('click', emergencyStop);
    $('#stopDance').on('click', stopDance);
    $('#danceButton').on('click', startDance);
    $('#globalStopAll').on('click', () => controlAllRobots('stop'));
    $('#globalForwardAll').on('click', () => controlAllRobots('forward'));
    $('#globalBackAll').on('click', () => controlAllRobots('backward'));
    $('#globalLeftAll').on('click', () => controlAllRobots('left'));
    $('#globalRightAll').on('click', () => controlAllRobots('right'));
    
    console.log("✅ System ready - Emergency stop available!");
});
