from flask import Flask, render_template, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

print("\n" + "="*70)
print("🤖 MULTI-ROBOT CONTROL SYSTEM")
print("="*70)

# ============================================
# ROBOT CONFIGURATION
# ============================================
# Add each robot's IP address and port
ROBOTS = {
    0: {
        'name': 'Robot 1',
        'ip': '10.202.105.234',  # Robot 1's IP
        'port': 5005,
        'active': True
    },
    1: {
        'name': 'Robot 2',
        'ip': '192.168.1.102',  # CHANGE THIS to Robot 2's IP
        'port': 5005,
        'active': True
    },
    # Add more robots here
    # 2: {'name': 'Robot 3', 'ip': '192.168.1.103', 'port': 5005, 'active': True},
}

# Test connection to all robots
def test_robot_connection(robot_id):
    robot = ROBOTS[robot_id]
    try:
        response = requests.get(f"http://{robot['ip']}:{robot['port']}/move/stop", timeout=2)
        return response.status_code == 200
    except:
        return False

# Send command to a specific robot
def send_to_robot(robot_id, direction):
    robot = ROBOTS[robot_id]
    url = f"http://{robot['ip']}:{robot['port']}/move/{direction}"
    try:
        response = requests.get(url, timeout=1)
        print(f"  ✅ {robot['name']}: {direction}")
        return True
    except Exception as e:
        print(f"  ❌ {robot['name']}: Failed - {e}")
        return False

# Send command to ALL robots
def send_to_all_robots(direction):
    results = {}
    for robot_id, robot in ROBOTS.items():
        if robot['active']:
            results[robot_id] = send_to_robot(robot_id, direction)
    return results

# ============================================
# FLASK ROUTES
# ============================================

@app.route("/")
def index():
    return render_template("index_multi.html")

@app.route("/status")
def status():
    # Test all robot connections
    robot_status = {}
    for robot_id, robot in ROBOTS.items():
        robot_status[robot_id] = {
            'name': robot['name'],
            'ip': robot['ip'],
            'online': test_robot_connection(robot_id)
        }
    return jsonify({
        'status': 'ok',
        'robots': robot_status,
        'total': len(ROBOTS)
    })

@app.route("/move/<int:robot_id>/<direction>")
def move_robot(robot_id, direction):
    """Control a specific robot"""
    if robot_id not in ROBOTS:
        return jsonify({'error': 'Robot not found'}), 404
    
    print(f"\n🤖 {ROBOTS[robot_id]['name']}: {direction.upper()}")
    success = send_to_robot(robot_id, direction)
    
    return jsonify({
        'status': 'ok' if success else 'error',
        'robot': robot_id,
        'direction': direction
    })

@app.route("/move/all/<direction>")
def move_all_robots(direction):
    """Control ALL robots simultaneously"""
    print(f"\n🌐 ALL ROBOTS: {direction.upper()}")
    results = send_to_all_robots(direction)
    
    return jsonify({
        'status': 'ok',
        'direction': direction,
        'results': results
    })

@app.route("/dance")
def dance():
    """Synchronized dance routine for all robots"""
    print("\n💃🕺 SYNC DANCE WITH ALL ROBOTS!")
    
    dance_steps = [
        ('forward', 0.4),
        ('backward', 0.4),
        ('left', 0.3),
        ('right', 0.3),
        ('forward', 0.3),
        ('backward', 0.3),
        ('stop', 0.2),
    ]
    
    def execute_dance():
        for direction, duration in dance_steps:
            print(f"  🎵 {direction.upper()}")
            send_to_all_robots(direction)
            time.sleep(duration)
        send_to_all_robots('stop')
        print("🎉 DANCE COMPLETE!")
    
    # Run dance in background thread
    dance_thread = threading.Thread(target=execute_dance)
    dance_thread.start()
    
    return jsonify({'status': 'ok', 'message': 'Dance started'})

@app.route("/emergency/stop")
def emergency_stop():
    """Emergency stop all robots"""
    print("\n🚨 EMERGENCY STOP ALL ROBOTS!")
    send_to_all_robots('stop')
    return jsonify({'status': 'ok', 'message': 'All robots stopped'})

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 MULTI-ROBOT CONTROL CENTER READY")
    print("="*70)
    print(f"📡 Web Interface: http://0.0.0.0:5005")
    print(f"🤖 Configured Robots: {len(ROBOTS)}")
    for robot_id, robot in ROBOTS.items():
        print(f"   - {robot['name']}: {robot['ip']}:{robot['port']}")
    print("\n🎮 Controls:")
    print("   - /move/0/forward - Control Robot 1")
    print("   - /move/1/forward - Control Robot 2")
    print("   - /move/all/forward - Control ALL robots")
    print("   - /dance - Synchronized dance")
    print("   - /emergency/stop - Stop ALL robots")
    print("="*70 + "\n")
    
    app.run(host="0.0.0.0", debug=False, port=5005)
