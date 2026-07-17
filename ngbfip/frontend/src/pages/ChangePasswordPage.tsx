import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Lock, AlertCircle, CheckCircle } from 'lucide-react'
import { authAPI } from '@/lib/api'
import '../styles/AuthPages.css'

function ChangePasswordPage() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    old_password: '',
    new_password: '',
    confirm_password: '',
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [success, setSuccess] = useState('')

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.old_password) newErrors.old_password = 'Current password is required'

    if (!formData.new_password) newErrors.new_password = 'New password is required'
    else if (formData.new_password.length < 8) {
      newErrors.new_password = 'Password must be at least 8 characters'
    }
    else if (!/[A-Z]/.test(formData.new_password)) {
      newErrors.new_password = 'Password must contain at least one uppercase letter'
    }
    else if (!/[a-z]/.test(formData.new_password)) {
      newErrors.new_password = 'Password must contain at least one lowercase letter'
    }
    else if (!/[0-9]/.test(formData.new_password)) {
      newErrors.new_password = 'Password must contain at least one digit'
    }

    if (!formData.confirm_password) {
      newErrors.confirm_password = 'Please confirm your new password'
    } else if (formData.new_password !== formData.confirm_password) {
      newErrors.confirm_password = 'Passwords do not match'
    }

    if (formData.old_password === formData.new_password) {
      newErrors.new_password = 'New password must be different from current password'
    }

    return newErrors
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }))
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: '',
      }))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrors({})

    const newErrors = validateForm()
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setIsLoading(true)

    try {
      await authAPI.changePassword(
        formData.old_password,
        formData.new_password,
        formData.confirm_password
      )

      setSuccess('Password changed successfully!')
      setTimeout(() => {
        navigate('/profile')
      }, 2000)
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to change password'
      setErrors({ submit: errorMessage })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-card">
          <div className="auth-header">
            <h1>Change Password</h1>
            <p>Update your account password</p>
          </div>

          {success && (
            <div className="success-message">
              <CheckCircle size={18} />
              {success}
            </div>
          )}

          <form onSubmit={handleSubmit} className="auth-form">
            {errors.submit && (
              <div className="error-message">
                <AlertCircle size={18} />
                {errors.submit}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="old_password">Current Password</label>
              <div className="input-wrapper">
                <Lock size={18} />
                <input
                  id="old_password"
                  type="password"
                  name="old_password"
                  placeholder="Enter your current password"
                  value={formData.old_password}
                  onChange={handleChange}
                  className={errors.old_password ? 'input-error' : ''}
                />
              </div>
              {errors.old_password && (
                <span className="field-error">{errors.old_password}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="new_password">New Password</label>
              <div className="input-wrapper">
                <Lock size={18} />
                <input
                  id="new_password"
                  type="password"
                  name="new_password"
                  placeholder="Create a new password"
                  value={formData.new_password}
                  onChange={handleChange}
                  className={errors.new_password ? 'input-error' : ''}
                />
              </div>
              {errors.new_password && (
                <span className="field-error">{errors.new_password}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="confirm_password">Confirm New Password</label>
              <div className="input-wrapper">
                <Lock size={18} />
                <input
                  id="confirm_password"
                  type="password"
                  name="confirm_password"
                  placeholder="Confirm your new password"
                  value={formData.confirm_password}
                  onChange={handleChange}
                  className={errors.confirm_password ? 'input-error' : ''}
                />
              </div>
              {errors.confirm_password && (
                <span className="field-error">{errors.confirm_password}</span>
              )}
            </div>

            <button type="submit" className="auth-btn" disabled={isLoading}>
              {isLoading ? 'Updating Password...' : 'Change Password'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ChangePasswordPage
