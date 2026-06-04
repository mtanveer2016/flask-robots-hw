// ============================================
// API CONFIGURATION
// ============================================
// Change this to your Raspberry Pi's IP address
const ROBOT_API_BASE = 'http://10.202.105.234:5005';

// Number of robots in your cluster
const ROBOT_COUNT = 10;

// Store active timeouts for each robot
let activeTimeouts = {};
let selectedRobotIndex = 0;
let isDancing = false;
let danceInterval = null;
let danceStepIndex = 0;

// ============================================
// COMMAND FUNCTIONS
// ============================================

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
    console.log(`[SELECT] Robot ${parseInt(robotId) + 1} selected`);
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

function startSyncDance() {
    if (isDancing) { stopSyncDance(); return; }
    isDancing = true;
    danceStepIndex = 0;
    $('.robot-card').addClass('dancing');
    
    const danceRoutine = [
        { cmd: 'forward', duration: 400 }, { cmd: 'backward', duration: 400 },
        { cmd: 'left', duration: 350 }, { cmd: 'right', duration: 350 },
        { cmd: 'forward', duration: 300 }, { cmd: 'backward', duration: 300 },
        { cmd: 'stop', duration: 150 }, { cmd: 'left', duration: 300 },
        { cmd: 'right', duration: 300 }, { cmd: 'forward', duration: 350 },
        { cmd: 'stop', duration: 200 }, { cmd: 'stop', duration: 400 }
    ];
    
    function executeDanceStep() {
        if (!isDancing || danceStepIndex >= danceRoutine.length) {
            stopSyncDance();
            return;
        }
        const step = danceRoutine[danceStepIndex];
        for (let i = 0; i < ROBOT_COUNT; i++) sendCommand(i, step.cmd);
        danceStepIndex++;
        danceInterval = setTimeout(executeDanceStep, step.duration);
    }
    executeDanceStep();
}

function stopSyncDance() {
    if (danceInterval) clearTimeout(danceInterval);
    isDancing = false;
    $('.robot-card').removeClass('dancing');
    for (let i = 0; i < ROBOT_COUNT; i++) sendCommand(i, 'stop');
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

$(document).ready(function() {
    console.log("🤖 Multi-Robot Control System Loaded");
    console.log(`🌐 API: ${ROBOT_API_BASE}`);
    console.log(`🤖 Robots: ${ROBOT_COUNT}`);
    renderRobotsGrid();
    setupEventDelegation();

$('#ledTest').on('click', function() {
    $.get(`${ROBOT_API_BASE}/led/test`);
});    
    $('#danceButton').on('click', startSyncDance);
    $('#globalStopAll').on('click', () => controlAllRobots('stop'));
    $('#globalForwardAll').on('click', () => controlAllRobots('forward'));
    $('#globalBackAll').on('click', () => controlAllRobots('backward'));
    $('#globalLeftAll').on('click', () => controlAllRobots('left'));
    $('#globalRightAll').on('click', () => controlAllRobots('right'));
    
});

