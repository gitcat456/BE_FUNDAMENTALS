import { lazy, Suspense, useCallback, useEffect, useRef, useState } from 'react'

import { useAuth } from '../../auth/AuthContext'

import {

  fetchUserProfile,

  updateUserProfile,

  uploadProfilePhoto,

  validateProfilePhoto,

} from '../../api/profileApi'

import type { UserProfileDetail } from '../../api/types'

import { useSnackbar } from '../../components/snackbar/SnackbarProvider'

import { EditableProfileField } from '../../components/profile/EditableProfileField'
import { DocumentUploadField } from '../../components/storage/DocumentUploadField'
import {
  downloadStoredFile,
  uploadProfileCv,
} from '../../api/storageApi'

const ProfileMap = lazy(() =>
  import('../../components/profile/ProfileMap').then((m) => ({ default: m.ProfileMap })),
)



function profileInitials(username: string): string {

  const parts = username.trim().split(/\s+/)

  if (parts.length >= 2) return `${parts[0][0] ?? ''}${parts[1][0] ?? ''}`.toUpperCase()

  return (username.slice(0, 2) || '?').toUpperCase()

}



function locationLabel(data: UserProfileDetail): string | null {

  return data.place_name ?? data.location ?? null

}



export function ProfilePage() {

  const { profile, refreshProfile } = useAuth()

  const { showSuccess, showError } = useSnackbar()

  const fileInputRef = useRef<HTMLInputElement>(null)



  const [profileData, setProfileData] = useState<UserProfileDetail | null>(null)

  const [loading, setLoading] = useState(true)

  const [uploadingPhoto, setUploadingPhoto] = useState(false)
  const [uploadingCv, setUploadingCv] = useState(false)



  const [bioEditing, setBioEditing] = useState(false)

  const [bioDraft, setBioDraft] = useState('')

  const [savingBio, setSavingBio] = useState(false)



  const [locationEditing, setLocationEditing] = useState(false)

  const [locationDraft, setLocationDraft] = useState('')

  const [savingLocation, setSavingLocation] = useState(false)



  const load = useCallback(async () => {

    setLoading(true)

    try {

      const data = await fetchUserProfile()

      setProfileData(data)

      setBioDraft(data.bio ?? '')

      setLocationDraft(data.location ?? '')

    } catch (e) {

      showError(e instanceof Error ? e.message : 'Could not load profile')

    } finally {

      setLoading(false)

    }

  }, [showError])



  useEffect(() => {

    void load()

  }, [load])



  if (!profile) return null



  const displayPhoto = profileData?.photo_url ?? profile.photo_url

  const hasCoords =

    profileData?.lat != null &&

    profileData?.lng != null &&

    Number.isFinite(profileData.lat) &&

    Number.isFinite(profileData.lng)



  function startBioEdit() {

    setBioDraft(profileData?.bio ?? '')

    setBioEditing(true)

  }



  function cancelBioEdit() {

    setBioDraft(profileData?.bio ?? '')

    setBioEditing(false)

  }



  async function saveBio() {

    setSavingBio(true)

    try {

      const data = await updateUserProfile({ bio: bioDraft.trim() })

      setProfileData(data)

      setBioDraft(data.bio ?? '')

      setBioEditing(false)

      await refreshProfile()

      showSuccess('Your bio was saved.')

    } catch (err) {

      showError(err instanceof Error ? err.message : 'Could not save bio')

    } finally {

      setSavingBio(false)

    }

  }



  function startLocationEdit() {

    setLocationDraft(profileData?.location ?? '')

    setLocationEditing(true)

  }



  function cancelLocationEdit() {

    setLocationDraft(profileData?.location ?? '')

    setLocationEditing(false)

  }



  async function saveLocation() {

    const trimmed = locationDraft.trim()

    if (!trimmed) {

      showError('Enter a location before saving.')

      return

    }

    setSavingLocation(true)

    try {

      const data = await updateUserProfile({ location: trimmed, country: 'KE' })

      setProfileData(data)

      setLocationDraft(data.location ?? '')

      setLocationEditing(false)

      await refreshProfile()

      showSuccess('Your location was saved.')

    } catch (err) {

      showError(err instanceof Error ? err.message : 'Could not save location')

    } finally {

      setSavingLocation(false)

    }

  }



  async function onCvUpload(file: File) {
    setUploadingCv(true)
    try {
      const result = await uploadProfileCv(file)
      setProfileData((prev) =>
        prev
          ? {
              ...prev,
              cv_filename: result.cv_filename,
              cv_object_name: result.cv_object_name,
            }
          : prev,
      )
      showSuccess('Document saved to your profile.')
    } catch (err) {
      showError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setUploadingCv(false)
    }
  }

  async function onCvDownload() {
    const objectName = profileData?.cv_object_name
    const filename = profileData?.cv_filename ?? 'document'
    if (!objectName) return
    try {
      await downloadStoredFile(objectName, filename)
    } catch (err) {
      showError(err instanceof Error ? err.message : 'Download failed')
    }
  }

  async function onPhotoSelected(file: File | undefined) {

    if (!file) return

    const validationError = validateProfilePhoto(file)

    if (validationError) {

      showError(validationError)

      return

    }

    setUploadingPhoto(true)

    try {

      const { photo_url } = await uploadProfilePhoto(file)

      setProfileData((prev) => (prev ? { ...prev, photo_url } : prev))

      await refreshProfile()

      showSuccess('Profile photo updated.')

    } catch (err) {

      showError(err instanceof Error ? err.message : 'Upload failed')

    } finally {

      setUploadingPhoto(false)

      if (fileInputRef.current) fileInputRef.current.value = ''

    }

  }



  return (

    <div className="max-w-xl">

      <p className="text-xs font-medium uppercase tracking-[0.2em] text-accent-dim">

        Account

      </p>

      <h1 className="mt-2 font-display text-3xl font-semibold text-ink">Your profile</h1>

      <p className="mt-3 text-sm leading-relaxed text-muted">

        Location is geocoded with Mapbox on save via{' '}

        <code className="text-accent">PATCH /api/users/profile/update/</code>.

      </p>



      <section className="mt-10 rounded-2xl border border-border bg-surface/80 p-6">

        <p className="text-sm font-medium text-ink">Profile photo</p>

        <div className="mt-5 flex flex-wrap items-center gap-6">

          <div className="relative size-28 shrink-0 overflow-hidden rounded-full border-2 border-border bg-canvas">

            {displayPhoto ? (

              <img src={displayPhoto} alt="" className="size-full object-cover" />

            ) : (

              <span className="flex size-full items-center justify-center font-display text-2xl font-semibold text-accent">

                {profileInitials(profile.username)}

              </span>

            )}

            {uploadingPhoto ? (

              <div className="absolute inset-0 flex items-center justify-center bg-black/50 text-xs font-medium text-white">

                Uploading…

              </div>

            ) : null}

          </div>

          <div className="min-w-0 flex-1">

            <p className="text-sm text-muted">

              JPEG, PNG, or WEBP · max 5MB · cropped to 400×400 on upload.

            </p>

            <input

              ref={fileInputRef}

              type="file"

              accept="image/jpeg,image/png,image/webp"

              className="sr-only"

              disabled={uploadingPhoto || loading}

              onChange={(e) => void onPhotoSelected(e.target.files?.[0])}

            />

            <button

              type="button"

              disabled={uploadingPhoto || loading}

              onClick={() => fileInputRef.current?.click()}

              className="mt-4 rounded-xl border border-border px-4 py-2 text-sm font-medium text-ink transition hover:border-accent-dim disabled:opacity-50"

            >

              {displayPhoto ? 'Change photo' : 'Upload photo'}

            </button>

          </div>

        </div>

      </section>

      <section className="mt-6">
        <DocumentUploadField
          label="Private documents"
          hint="PDF, Word, or video · max 10MB · stored securely in MinIO via presigned upload."
          existingFilename={profileData?.cv_filename}
          disabled={loading}
          uploading={uploadingCv}
          onUpload={onCvUpload}
          onDownload={profileData?.cv_object_name ? onCvDownload : undefined}
        />
      </section>

      <section className="mt-6 rounded-2xl border border-border bg-surface/80 p-6">

        <p className="text-sm font-medium text-ink">Account details</p>

        <dl className="mt-4 space-y-3 text-sm">

          <div className="flex gap-3">

            <dt className="w-24 shrink-0 text-muted">Username</dt>

            <dd className="text-ink">{profile.username}</dd>

          </div>

          <div className="flex gap-3">

            <dt className="w-24 shrink-0 text-muted">Email</dt>

            <dd className="truncate text-ink">{profile.email}</dd>

          </div>

          <div className="flex gap-3">

            <dt className="w-24 shrink-0 text-muted">Role</dt>

            <dd className="capitalize text-ink">{profile.role}</dd>

          </div>

        </dl>

      </section>



      <div className="mt-6 space-y-6">

        <EditableProfileField

          label="Bio"

          display={profileData?.bio?.trim() ? profileData.bio : null}

          emptyLabel="No bio yet"

          editing={bioEditing}

          disabled={loading}

          saving={savingBio}

          onEdit={startBioEdit}

          onCancel={cancelBioEdit}

          onSave={() => void saveBio()}

        >

          <textarea

            id="profile-bio"

            value={bioDraft}

            onChange={(e) => setBioDraft(e.target.value)}

            disabled={loading || savingBio}

            rows={4}

            placeholder="A short note about you…"

            className="w-full resize-y rounded-lg border border-border bg-canvas px-3 py-2.5 text-sm text-ink outline-none transition focus:border-accent-dim disabled:opacity-50"

          />

        </EditableProfileField>



        <EditableProfileField

          label="Location"

          display={

            profileData && locationLabel(profileData) ? (

              <div className="space-y-4">

                <p>{locationLabel(profileData)}</p>

                {hasCoords ? (
                  <Suspense
                    fallback={
                      <div className="h-48 animate-pulse rounded-xl border border-border bg-canvas" />
                    }
                  >
                    <ProfileMap lat={profileData!.lat!} lng={profileData!.lng!} />
                  </Suspense>
                ) : null}

              </div>

            ) : null

          }

          emptyLabel="No location set"

          editing={locationEditing}

          disabled={loading}

          saving={savingLocation}

          onEdit={startLocationEdit}

          onCancel={cancelLocationEdit}

          onSave={() => void saveLocation()}

        >

          <input

            id="profile-location"

            type="text"

            value={locationDraft}

            onChange={(e) => setLocationDraft(e.target.value)}

            disabled={loading || savingLocation}

            placeholder="e.g. Westlands, Nairobi"

            className="w-full rounded-lg border border-border bg-canvas px-3 py-2.5 text-sm text-ink outline-none transition focus:border-accent-dim disabled:opacity-50"

          />

          <p className="mt-2 text-xs text-muted">

            We geocode your address with Mapbox when you save. Be specific for better results.

          </p>

        </EditableProfileField>

      </div>

    </div>

  )

}


