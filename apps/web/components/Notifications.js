'use client'
import { useEffect, useState } from 'react'

export default function Notifications({ hearings = [] }) {
  const [notifications, setNotifications] = useState([])
  const [show, setShow] = useState(false)

  useEffect(() => {
    const checkUpcomingHearings = () => {
      const now = new Date()
      const upcoming = []

      hearings.forEach(hearing => {
        if (!hearing.starts_at) return

        const hearingDate = new Date(hearing.starts_at)
        const diffTime = hearingDate - now
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

        // Notify for hearings in the next 7 days
        if (diffDays >= 0 && diffDays <= 7) {
          let urgency = 'normal'
          if (diffDays === 0) urgency = 'urgent'
          else if (diffDays === 1) urgency = 'warning'

          upcoming.push({
            id: hearing.id,
            court: hearing.court || 'Court not specified',
            purpose: hearing.purpose || 'Hearing',
            date: hearingDate,
            daysUntil: diffDays,
            urgency
          })
        }
      })

      setNotifications(upcoming.sort((a, b) => a.daysUntil - b.daysUntil))
    }

    checkUpcomingHearings()
    const interval = setInterval(checkUpcomingHearings, 60000) // Check every minute

    return () => clearInterval(interval)
  }, [hearings])

  if (notifications.length === 0) return null

  return (
    <div className="notifications-container">
      <button className="notification-bell" onClick={() => setShow(!show)}>
        <span className="bell-icon">🔔</span>
        {notifications.length > 0 && (
          <span className="notification-badge">{notifications.length}</span>
        )}
      </button>

      {show && (
        <div className="notifications-dropdown">
          <div className="notifications-header">
            <h4>Upcoming Hearings</h4>
            <button onClick={() => setShow(false)}>×</button>
          </div>
          <div className="notifications-list">
            {notifications.map(notif => (
              <div key={notif.id} className={`notification-item ${notif.urgency}`}>
                <div className="notification-icon">
                  {notif.urgency === 'urgent' && '🚨'}
                  {notif.urgency === 'warning' && '⚠️'}
                  {notif.urgency === 'normal' && '📅'}
                </div>
                <div className="notification-content">
                  <strong>{notif.purpose}</strong>
                  <p>{notif.court}</p>
                  <span className="notification-time">
                    {notif.daysUntil === 0 ? 'Today' :
                     notif.daysUntil === 1 ? 'Tomorrow' :
                     `In ${notif.daysUntil} days`}
                    {' - '}
                    {notif.date.toLocaleDateString()} at {notif.date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
