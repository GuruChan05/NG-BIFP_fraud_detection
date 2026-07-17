import { useState, useEffect, useRef } from 'react'
import { Bell, X, CheckCheck } from 'lucide-react'
import { notificationAPI } from '@/lib/api'
import '../styles/NotificationDropdown.css'

function NotificationDropdown() {
  const [isOpen, setIsOpen] = useState(false)
  const [notifications, setNotifications] = useState<any[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const loadNotifications = async () => {
      try {
        const response = await notificationAPI.list()
        setNotifications(response.data)
        const unread = response.data.filter((n: any) => !n.is_read).length
        setUnreadCount(unread)
      } catch (err) {
        console.error('Failed to load notifications:', err)
      }
    }

    loadNotifications()
    // Poll for new notifications every 30 seconds
    const interval = setInterval(loadNotifications, 30000)

    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen])

  const handleMarkAsRead = async (notificationId: number) => {
    try {
      await notificationAPI.markAsRead(notificationId)
      setNotifications(prev =>
        prev.map(n => (n.id === notificationId ? { ...n, is_read: true } : n))
      )
      setUnreadCount(prev => Math.max(0, prev - 1))
    } catch (err) {
      console.error('Failed to mark notification as read:', err)
    }
  }

  const handleDelete = async (notificationId: number) => {
    try {
      await notificationAPI.delete(notificationId)
      setNotifications(prev => prev.filter(n => n.id !== notificationId))
    } catch (err) {
      console.error('Failed to delete notification:', err)
    }
  }

  const handleMarkAllAsRead = async () => {
    try {
      await notificationAPI.markAllAsRead()
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })))
      setUnreadCount(0)
    } catch (err) {
      console.error('Failed to mark all as read:', err)
    }
  }

  return (
    <div className="notification-dropdown" ref={dropdownRef}>
      <button
        className="notification-bell"
        onClick={() => setIsOpen(!isOpen)}
        title="Notifications"
      >
        <Bell size={20} />
        {unreadCount > 0 && <span className="unread-badge">{unreadCount}</span>}
      </button>

      {isOpen && (
        <div className="notification-panel">
          <div className="notification-header">
            <h3>Notifications</h3>
            {unreadCount > 0 && (
              <button
                className="mark-all-btn"
                onClick={handleMarkAllAsRead}
                title="Mark all as read"
              >
                <CheckCheck size={16} />
              </button>
            )}
          </div>

          {notifications.length === 0 ? (
            <div className="no-notifications">No notifications</div>
          ) : (
            <div className="notification-list">
              {notifications.map(notification => (
                <div
                  key={notification.id}
                  className={`notification-item ${!notification.is_read ? 'unread' : ''}`}
                >
                  <div className="notification-content">
                    <h4>{notification.title}</h4>
                    <p>{notification.message}</p>
                    <small>{new Date(notification.created_at).toLocaleDateString()}</small>
                  </div>
                  <div className="notification-actions">
                    {!notification.is_read && (
                      <button
                        className="mark-read-btn"
                        onClick={() => handleMarkAsRead(notification.id)}
                        title="Mark as read"
                      >
                        <CheckCheck size={16} />
                      </button>
                    )}
                    <button
                      className="delete-btn"
                      onClick={() => handleDelete(notification.id)}
                      title="Delete"
                    >
                      <X size={16} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default NotificationDropdown
