from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

notifications = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'notification-service'}), 200

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    notification_type = data.get('type', 'info')
    recipient = data.get('recipient', '')
    subject = data.get('subject', '')
    message = data.get('message', '')
    
    notification = {
        'id': len(notifications) + 1,
        'type': notification_type,
        'recipient': recipient,
        'subject': subject,
        'message': message,
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'sent'
    }
    
    notifications.append(notification)
    print(f"[NOTIFICATION] {notification_type.upper()} to {recipient}: {subject} - {message}")
    
    return jsonify({
        'status': 'success',
        'notification_id': notification['id'],
        'message': 'Уведомление отправлено'
    }), 201

@app.route('/notifications', methods=['GET'])
def get_notifications():
    return jsonify({'notifications': notifications}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)