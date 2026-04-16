// Store active timeouts for each robot
let activeTimeouts = {};
let selectedRobotIndex = 0;
let isDancing = false;
let danceInterval = null;
let danceStepIndex = 0;

// ============================================
// FIXED: Using EVENT DELEGATION for dynamic elements
// ============================================

// Function to send command to a specific robot
function sendCommand(robotId, command) {
    console.log(`[CMD] Robot ${robotId}: ${command}`);
    
    $.get(`/move/${robotId}/${command}`, function(data) {
        console.log(`[OK] Robot ${robotId}: ${command}`);
        showRobotFeedback(robotId, command);
    }).fail(function(err) {
        console.error(`[ERR] Robot ${robotId}:`, err);
        showRobotFeedback(robotId, 'error');
    });
}

// Show visual feedback on robot card
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
    
    // Remove existing feedback
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
    
    setTimeout(() => {
        feedback.fadeOut(300, function() { $(this).remove(); });
    }, duration);
}

// ============================================
// FIXED: Set selected robot (works with dynamic content)
// ============================================
function setSelectedRobot(robotId) {
    if (robotId === undefined || robotId === null) return;
    
    selectedRobotIndex = robotId;
    
    // Remove selected class from all cards
    $('.robot-card').removeClass('selected');
    
    // Add selected class to the clicked card
    $(`.robot-card[data-robot-idx="${robotId}"]`).addClass('selected');
    
    // Update the display
    $('#selectedRobotId').text(`ROBOT ${parseInt(robotId) + 1}`);
    console.log(`[SELECT] Robot ${parseInt(robotId) + 1} selected`);
    
    // Optional: Add a subtle highlight effect
    showGlobalNotification(`🎯 Robot ${parseInt(robotId) + 1} selected`, "#3498db", 1000);
}

// ============================================
// FIXED: Using EVENT DELEGATION (handles dynamic elements)
// ============================================

function setupEventDelegation() {
    // Handle SELECT button clicks using event delegation
    $(document).on('click', '[id^="select-"]', function() {
        const buttonId = $(this).attr('id');
        const robotId = buttonId.split('-')[1];
        console.log(`[UI] Select button clicked for robot ${robotId}`);
        setSelectedRobot(parseInt(robotId));
    });
    
    // Handle STOP button clicks
    $(document).on('click', '[id^="stop-"]', function() {
        const buttonId = $(this).attr('id');
        const robotId = buttonId.split('-')[1];
        console.log(`[UI] Stop button clicked for robot ${robotId}`);
        if (activeTimeouts[robotId]) clearTimeout(activeTimeouts[robotId]);
        sendCommand(parseInt(robotId), 'stop');
        showRobotFeedback(parseInt(robotId), 'stop', 500);
    });
    
    // Handle D-pad buttons using event delegation
    $(document).on('mousedown touchstart', '[id^="forward-"]', function(e) {
        e.preventDefault();
        const buttonId = $(this).attr('id');
        const robotId = buttonId.split('-')[1];
        if (activeTimeouts[robotId]) clearTimeout(activeTimeouts[robotId]);
        sendCommand(parseInt(robotId), 'forward');
        showRobotFeedback(parseInt(robotId), 'forward');
    });
    
    $(document).on('mouseup touchend', '[id^="forward-"]', function(e) {
        e.preventDefault();
        const buttonId = $(this).attr('id');
        const robotId = buttonId.split('-')[1];
        activeTimeouts[robotId] = setTimeout(() => {
            sendCommand(parseInt(robotId), 'stop');
        }, 50);
    });
    
    $(document).on('mousedown touchstart', '[id^="backward-"]', function(e) {
        e.preventDefault();
        const buttonId = $(this).attr('id');
        const robotId = buttonId.split('-')[1];
        if (activeTimeouts[robotId]) clearTimeout(activeTimeouts[robotId]);
        sendCommand(parseInt(robotId), 'backward');
        showRobotFeedback(parseInt(robotId), 'backward');
    });
    
    $(document).on('mouseup touchend', '[id^="backward-"]', function(e) {
        e.preventDefault();
        const buttonId = $(this).attr('id');
        const robotId = buttonId.split('-')[1];
        activeTimeouts[robotId] = setTimeout(() => {
            sendCommand(parseInt(robotId), 'stop');
        }, 50);
    });
    
    $(document).on('mousedown touchstart', '[id^="left-"]', function(e) {
        e.preventDefault();
        const buttonId = $(this).attr('id');
        const robotId = buttonId.split('-')[1];
        if (activeTimeouts[robotId]) clearTimeout(activeTimeouts[robotId]);
        sendCommand(parseInt(robotId), 'left');
        showRobotFeedback(parseInt(robotId), 'left');
    });
    
    $(document).on('mouseup touchend', '[id^="left-"]', function(e) {
        e.preventDefault();
        const buttonId = $(this).attr('id');
        const robotId = buttonId.split('-')[1];
        activeTimeouts[robotId] = setTimeout(() => {
            sendCommand(parseInt(robotId), 'stop');
        }, 50);
    });
    
    $(document).on('mousedown touchstart', '[id^="right-"]', function(e) {
        e.preventDefault();
        const buttonId = $(this).attr('id');
        const robotId = buttonId.split('-')[1];
        if (activeTimeouts[robotId]) clearTimeout(activeTimeouts[robotId]);
        sendCommand(parseInt(robotId), 'right');
        showRobotFeedback(parseInt(robotId), 'right');
    });
    
    $(document).on('mouseup touchend', '[id^="right-"]', function(e) {
        e.preventDefault();
        const buttonId = $(this).attr('id');
        const robotId = buttonId.split('-')[1];
        activeTimeouts[robotId] = setTimeout(() => {
            sendCommand(parseInt(robotId), 'stop');
        }, 50);
    });
    
    // Handle speed sliders
    $(document).on('input', '[id^="speed-"]', function() {
        const sliderId = $(this).attr('id');
        const robotId = sliderId.split('-')[1];
        let speed = $(this).val();
        $(`#speed-value-${robotId}`).text(speed);
        $(`#speed-display-${robotId}`).text(speed);
        console.log(`[SPEED] Robot ${robotId}: ${speed}/10`);
        $.get(`/speed/${robotId}/${speed}`);
    });
    
    // Handle clicking on robot card to select
    $(document).on('click', '.robot-card', function(e) {
        // Don't trigger if clicking on buttons inside the card
        if ($(e.target).is('button') || $(e.target).is('input')) {
            return;
        }
        const robotId = $(this).attr('data-robot-idx');
        if (robotId !== undefined) {
            console.log(`[UI] Card clicked for robot ${robotId}`);
            setSelectedRobot(parseInt(robotId));
        }
    });
}

// ============================================
// DANCE ROUTINE (Same as before)
// ============================================

function startSyncDance() {
    if (isDancing) {
        console.log("[DANCE] Already dancing! Stopping...");
        stopSyncDance();
        return;
    }
    
    console.log("\n" + "🎵".repeat(30));
    console.log("💃🕺 SYNC DANCE PARTY STARTED! 🎵🎶");
    console.log("🎵".repeat(30));
    
    isDancing = true;
    danceStepIndex = 0;
    
    // Add dancing animation to all robot cards
    $('.robot-card').addClass('dancing');
    showGlobalNotification("💃🕺 ALL ROBOTS DANCING! 🎵🎶", "#e74c3c", 2000);
    
    const danceRoutine = [
        { cmd: 'forward', duration: 400, msg: '⬆️ FORWARD STEP!' },
        { cmd: 'backward', duration: 400, msg: '⬇️ BACKWARD STEP!' },
        { cmd: 'left', duration: 350, msg: '⬅️ TURN LEFT!' },
        { cmd: 'right', duration: 350, msg: '➡️ TURN RIGHT!' },
        { cmd: 'forward', duration: 300, msg: '⬆️ QUICK FORWARD!' },
        { cmd: 'backward', duration: 300, msg: '⬇️ QUICK BACK!' },
        { cmd: 'stop', duration: 150, msg: '⏸️ PAUSE...' },
        { cmd: 'left', duration: 300, msg: '⬅️ SPIN LEFT!' },
        { cmd: 'right', duration: 300, msg: '➡️ SPIN RIGHT!' },
        { cmd: 'forward', duration: 350, msg: '⬆️ MARCH FORWARD!' },
        { cmd: 'stop', duration: 200, msg: '🎵 READY...' },
        { cmd: 'left', duration: 250, msg: '⬅️ DIP LEFT!' },
        { cmd: 'right', duration: 250, msg: '➡️ DIP RIGHT!' },
        { cmd: 'forward', duration: 300, msg: '⬆️ FINAL STEP!' },
        { cmd: 'stop', duration: 400, msg: '🎉 GRAND FINALE! 🎉' }
    ];
    
    function executeDanceStep() {
        if (!isDancing) return;
        
        if (danceStepIndex >= danceRoutine.length) {
            console.log("\n🎉 DANCE COMPLETE! 🎉\n");
            showGlobalNotification("🎉 Dance Complete! Robots resting 🎉", "#2ecc71", 2000);
            stopSyncDance();
            return;
        }
        
        const step = danceRoutine[danceStepIndex];
        console.log(`[DANCE] Step ${danceStepIndex + 1}: ${step.msg}`);
        
        for (let i = 0; i < 10; i++) {
            sendCommand(i, step.cmd);
            if (step.cmd !== 'stop') {
                showRobotFeedback(i, step.cmd, 300);
            }
        }
        
        danceStepIndex++;
        danceInterval = setTimeout(executeDanceStep, step.duration);
    }
    
    executeDanceStep();
}

function stopSyncDance() {
    if (danceInterval) {
        clearTimeout(danceInterval);
        danceInterval = null;
    }
    
    isDancing = false;
    $('.robot-card').removeClass('dancing');
    
    for (let i = 0; i < 10; i++) {
        sendCommand(i, 'stop');
    }
    
    console.log("[DANCE] Dance routine stopped");
}

// ============================================
// GLOBAL CONTROLS
// ============================================

function controlAllRobots(command) {
    if (isDancing) {
        showGlobalNotification("⏹️ Stopping dance first...", "#f39c12", 1000);
        stopSyncDance();
        setTimeout(() => controlAllRobots(command), 500);
        return;
    }
    
    console.log(`[GLOBAL] All robots: ${command}`);
    showGlobalNotification(`🌐 All robots: ${command.toUpperCase()}`, "#2c3e66", 1500);
    
    for (let i = 0; i < 10; i++) {
        sendCommand(i, command);
        showRobotFeedback(i, command, 400);
    }
}

function stopAllRobots() {
    if (isDancing) {
        stopSyncDance();
    }
    
    console.log(`[GLOBAL] STOP ALL ROBOTS`);
    showGlobalNotification(`🛑 ALL ROBOTS STOPPED`, "#dc2626", 1500);
    
    for (let i = 0; i < 10; i++) {
        sendCommand(i, 'stop');
        if (activeTimeouts[i]) clearTimeout(activeTimeouts[i]);
    }
}

// ============================================
// NOTIFICATION SYSTEM
// ============================================

function showGlobalNotification(message, bgColor = "#333", duration = 2000) {
    let notification = $('#globalNotification');
    if (!notification.length) {
        notification = $(`<div id="globalNotification" style="position:fixed;bottom:30px;left:50%;transform:translateX(-50%);color:white;padding:12px 24px;border-radius:50px;z-index:9999;font-weight:bold;box-shadow:0 4px 12px rgba(0,0,0,0.3);"></div>`);
        $('body').append(notification);
    }
    notification.css('background', bgColor);
    notification.text(message).fadeIn(200);
    setTimeout(() => notification.fadeOut(500), duration);
}

// ============================================
// RENDER ROBOTS GRID
// ============================================

function renderRobotsGrid() {
    const grid = $('#robotsGrid');
    grid.empty();
    
    for (let i = 0; i < 10; i++) {
        const robotCard = `
            <div class="robot-card" data-robot-idx="${i}">
                <div class="robot-header">
                    <span class="robot-name">🤖 ROBOT ${i+1}</span>
                    <span class="robot-status"><span class="status-led"></span> active</span>
                </div>
                <div class="speed-preview">
                    🎚️ Current Speed: <strong id="speed-display-${i}">5.0</strong> / 10
                </div>
                <div class="dpad">
                    <table>
                        <tr>
                            <th></th>
                            <th><button id="forward-${i}" class="dpad-btn">▲</button></th>
                            <th></th>
                        </tr>
                        <tr>
                            <td><button id="left-${i}" class="dpad-btn">◀</button></td>
                            <td></td>
                            <td><button id="right-${i}" class="dpad-btn">▶</button></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td><button id="backward-${i}" class="dpad-btn">▼</button></td>
                            <td></td>
                        </tr>
                    </table>
                </div>
                <div class="speed-control">
                    <label style="font-size:0.75rem; font-weight:600;">⚙️ Speed (0-10):</label>
                    <input type="range" id="speed-${i}" min="0" max="10" step="0.5" value="5.0">
                    <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                        <span>🚀 Movement Speed</span>
                        <span class="speed-value" id="speed-value-${i}">5.0</span>
                    </div>
                </div>
                <div class="action-buttons">
                    <button id="select-${i}" class="select-btn">✅ Select</button>
                    <button id="stop-${i}" class="stop-btn">⏹️ Stop</button>
                </div>
            </div>
        `;
        grid.append(robotCard);
    }
    
    // Select first robot by default
    setSelectedRobot(0);
}

// ============================================
// INITIALIZATION
// ============================================

$(document).ready(function() {
    console.log("\n" + "=".repeat(60));
    console.log("🤖 MULTI-ROBOT COMMAND CENTER");
    console.log("=".repeat(60));
    
    // Render the grid
    renderRobotsGrid();
    
    // Set up event delegation (handles all dynamic elements)
    setupEventDelegation();
    
    // Global button handlers (these are static, so direct binding is fine)
    $('#danceButton').on('click', function() {
        console.log("[UI] SYNC DANCE button clicked!");
        startSyncDance();
    });
    
    $('#globalStopAll').on('click', function() {
        stopAllRobots();
    });
    
    $('#globalForwardAll').on('click', function() {
        controlAllRobots('forward');
    });
    
    $('#globalBackAll').on('click', function() {
        controlAllRobots('backward');
    });
    
    $('#globalLeftAll').on('click', function() {
        controlAllRobots('left');
    });
    
    $('#globalRightAll').on('click', function() {
        controlAllRobots('right');
    });
    
    console.log("✅ System ready! You can now select any robot card");
    console.log("💡 Click on any robot card or its SELECT button");
    console.log("=".repeat(60));
});