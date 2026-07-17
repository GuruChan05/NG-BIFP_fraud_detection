import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { User, Mail, Phone, Building2, Edit2, Save, X, Camera } from 'lucide-react'
import { useAuthStore } from '@/stores/auth.store'
import { userAPI } from '@/lib/api'
import '../styles/UserProfile.css'

function UserProfilePage() {
  const navigate = useNavigate()
  const { user: authUser } = useAuthStore()
  const [profile, setProfile] = useState<any>(null)
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const [formData, setFormData] = useState({
    full_name: '',
    bio: '',
    phone_number: '',
    department: '',
    avatar_url: '',
  })

  useEffect(() => {
    const loadProfile = async () => {
      try {
        setIsLoading(true)
        const response = await userAPI.getCurrentUser()
        setProfile(response.data)
        setFormData({
          full_name: response.data.full_name,
          bio: response.data.bio || '',
          phone_number: response.data.phone_number || '',
          department: response.data.department || '',
          avatar_url: response.data.avatar_url || '',
        })
      } catch (err: any) {
        setError('Failed to load profile')
      } finally {
        setIsLoading(false)
      }
    }

    if (authUser) {
      loadProfile()
    } else {
      navigate('/login')
    }
  }, [authUser, navigate])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleAvatarChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      // In a real app, upload to cloud storage
      const reader = new FileReader()
      reader.onload = (event) => {
        setFormData(prev => ({
          ...prev,
          avatar_url: event.target?.result as string,
        }))
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSave = async () => {
    try {
      setIsSaving(true)
      await userAPI.updateProfile(formData)
      setProfile({ ...profile, ...formData })
      setIsEditing(false)
      setSuccess('Profile updated successfully')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err: any) {
      setError('Failed to update profile')
    } finally {
      setIsSaving(false)
    }
  }

  if (isLoading) {
    return <div className="profile-page"><div className="loading">Loading profile...</div></div>
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        {error && <div className="error-alert">{error}</div>}
        {success && <div className="success-alert">{success}</div>}

        {/* Avatar Section */}
        <div className="profile-header">
          <div className="avatar-wrapper">
            <img
              src={formData.avatar_url || 'https://via.placeholder.com/150'}
              alt="User avatar"
              className="avatar"
            />
            {isEditing && (
              <label className="avatar-upload">
                <Camera size={20} />
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleAvatarChange}
                  hidden
                />
              </label>
            )}
          </div>
          <div className="profile-header-info">
            <h1>{profile?.full_name}</h1>
            <p className="email">{profile?.email}</p>
            <p className="username">@{profile?.username}</p>
          </div>
        </div>

        {/* Profile Details */}
        <div className="profile-section">
          <div className="section-header">
            <h2>Profile Information</h2>
            <button
              className="edit-btn"
              onClick={() => {
                if (isEditing) {
                  handleSave()
                } else {
                  setIsEditing(true)
                }
              }}
              disabled={isSaving}
            >
              {isEditing ? (
                <>
                  <Save size={16} />
                  Save
                </>
              ) : (
                <>
                  <Edit2 size={16} />
                  Edit
                </>
              )}
            </button>
            {isEditing && (
              <button
                className="cancel-btn"
                onClick={() => {
                  setIsEditing(false)
                  setFormData({
                    full_name: profile.full_name,
                    bio: profile.bio || '',
                    phone_number: profile.phone_number || '',
                    department: profile.department || '',
                    avatar_url: profile.avatar_url || '',
                  })
                }}
              >
                <X size={16} />
                Cancel
              </button>
            )}
          </div>

          <div className="profile-form">
            <div className="form-group">
              <label>
                <User size={18} />
                Full Name
              </label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>

            <div className="form-group">
              <label>
                <Mail size={18} />
                Email
              </label>
              <input
                type="email"
                value={profile?.email}
                disabled
              />
              <small>Email cannot be changed</small>
            </div>

            <div className="form-group">
              <label>
                <Phone size={18} />
                Phone Number
              </label>
              <input
                type="tel"
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
                placeholder="+1 (555) 000-0000"
                disabled={!isEditing}
              />
            </div>

            <div className="form-group">
              <label>
                <Building2 size={18} />
                Department
              </label>
              <input
                type="text"
                name="department"
                value={formData.department}
                onChange={handleChange}
                placeholder="Enter your department"
                disabled={!isEditing}
              />
            </div>

            <div className="form-group">
              <label>Bio</label>
              <textarea
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                placeholder="Tell us about yourself"
                disabled={!isEditing}
                rows={4}
              />
            </div>
          </div>
        </div>

        {/* Account Status */}
        <div className="profile-section">
          <h2>Account Status</h2>
          <div className="status-grid">
            <div className="status-item">
              <span className="label">Account Status</span>
              <span className="value active">{profile?.is_active ? 'Active' : 'Inactive'}</span>
            </div>
            <div className="status-item">
              <span className="label">Account Type</span>
              <span className="value">{profile?.is_admin ? 'Administrator' : 'User'}</span>
            </div>
            <div className="status-item">
              <span className="label">Verified</span>
              <span className="value">{profile?.is_verified ? 'Yes' : 'No'}</span>
            </div>
            <div className="status-item">
              <span className="label">Member Since</span>
              <span className="value">{new Date(profile?.created_at).toLocaleDateString()}</span>
            </div>
          </div>
        </div>

        {/* Security Options */}
        <div className="profile-section">
          <h2>Security</h2>
          <button
            className="security-btn"
            onClick={() => navigate('/change-password')}
          >
            Change Password
          </button>
        </div>
      </div>
    </div>
  )
}

export default UserProfilePage
