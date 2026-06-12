import { apiJson } from './client'

export const ALLOWED_DOCUMENT_TYPES = [
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'video/mp4',
  'video/webm',
  'video/quicktime',
] as const

export const ALLOWED_DOCUMENT_ACCEPT = [
  '.pdf',
  '.doc',
  '.docx',
  '.mp4',
  '.webm',
  '.mov',
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'video/mp4',
  'video/webm',
  'video/quicktime',
].join(',')

const MAX_DOCUMENT_BYTES = 10 * 1024 * 1024

export type PresignedUploadResponse = {
  upload_url: string
  upload_fields: Record<string, string>
  object_name: string
  expires_in: string
}

export type ConfirmProfileDocumentResponse = {
  message: string
  cv_filename: string
  cv_object_name: string
}

export type ConfirmBookDocumentResponse = {
  message: string
  book_id: number
  digital_filename: string
  digital_object_name: string
}

export function validateDocumentFile(file: File): string | null {
  if (!ALLOWED_DOCUMENT_TYPES.includes(file.type as (typeof ALLOWED_DOCUMENT_TYPES)[number])) {
    return 'Allowed types: PDF, Word (.doc/.docx), or video (MP4, WebM, MOV).'
  }
  if (file.size > MAX_DOCUMENT_BYTES) {
    return 'File must be 10MB or smaller.'
  }
  return null
}

export async function requestUploadUrl(body: {
  filename: string
  content_type: string
  folder: string
}): Promise<PresignedUploadResponse> {
  return apiJson<PresignedUploadResponse>('/storage/upload-url/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
}

async function uploadToPresignedPost(
  uploadUrl: string,
  fields: Record<string, string>,
  file: File,
): Promise<void> {
  const form = new FormData()
  for (const [key, value] of Object.entries(fields)) {
    form.append(key, value)
  }
  form.append('file', file)

  const res = await fetch(uploadUrl, { method: 'POST', body: form })
  if (!res.ok) {
    throw new Error('Upload to storage failed')
  }
}

export async function uploadDocumentViaPresignedUrl(
  file: File,
  folder: string,
): Promise<string> {
  const validationError = validateDocumentFile(file)
  if (validationError) throw new Error(validationError)

  const presigned = await requestUploadUrl({
    filename: file.name,
    content_type: file.type,
    folder,
  })

  await uploadToPresignedPost(presigned.upload_url, presigned.upload_fields, file)
  return presigned.object_name
}

export async function confirmProfileDocument(body: {
  object_name: string
  filename: string
  document_type?: 'cv'
}): Promise<ConfirmProfileDocumentResponse> {
  return apiJson<ConfirmProfileDocumentResponse>('/storage/confirm-document/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
}

export async function confirmBookDocument(body: {
  object_name: string
  book_id: number
  filename: string
}): Promise<ConfirmBookDocumentResponse> {
  return apiJson<ConfirmBookDocumentResponse>('/storage/confirm-book-document/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
}

export async function getDownloadUrl(objectName: string): Promise<string> {
  const params = new URLSearchParams({ object_name: objectName })
  const data = await apiJson<{ download_url: string }>(`/storage/download-url/?${params}`)
  return data.download_url
}

export async function downloadStoredFile(objectName: string, filename: string): Promise<void> {
  const url = await getDownloadUrl(objectName)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.rel = 'noopener'
  link.target = '_blank'
  document.body.appendChild(link)
  link.click()
  link.remove()
}

export async function uploadProfileCv(file: File): Promise<ConfirmProfileDocumentResponse> {
  const objectName = await uploadDocumentViaPresignedUrl(file, 'documents')
  return confirmProfileDocument({
    object_name: objectName,
    filename: file.name,
    document_type: 'cv',
  })
}

export async function uploadBookDigitalResource(
  file: File,
  bookId: number,
): Promise<ConfirmBookDocumentResponse> {
  const objectName = await uploadDocumentViaPresignedUrl(file, `books/book_${bookId}`)
  return confirmBookDocument({
    object_name: objectName,
    book_id: bookId,
    filename: file.name,
  })
}
