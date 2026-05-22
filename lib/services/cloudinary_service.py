import cloudinary.uploader


def upload_image(file, folder="general", public_id=None):
    """
    Upload any image to Cloudinary.
    
    file      → the actual file object from request.FILES
    folder    → organizes uploads in Cloudinary dashboard
    public_id → custom filename (optional, Cloudinary generates one if None)
    
    Returns the secure URL string or raises an exception.
    """
    result = cloudinary.uploader.upload(
        file,
        folder=folder,
        public_id=public_id,
        overwrite=True,
        resource_type="image",
        transformation=[
            {'quality': 'auto'},   # auto compress
            {'fetch_format': 'auto'}  # auto convert to webp/avif
        ]
    )
    return result['secure_url']


def upload_profile_photo(file, user_id):
    """Profile photos → square crop, 400x400"""
    result = cloudinary.uploader.upload(
        file,
        folder="profile_photos",
        public_id=f"user_{user_id}",  # deterministic — overwrites old photo
        overwrite=True,
        transformation=[
            {'width': 400, 'height': 400, 'crop': 'fill', 'gravity': 'face'},
            {'quality': 'auto'},
            {'fetch_format': 'auto'}
        ]
    )
    return result['secure_url']


def upload_product_image(file, product_id):
    """Product images → 800x800 square, clean crop"""
    result = cloudinary.uploader.upload(
        file,
        folder="product_images",
        public_id=f"product_{product_id}",
        overwrite=True,
        transformation=[
            {'width': 800, 'height': 800, 'crop': 'fill'},
            {'quality': 'auto'},
            {'fetch_format': 'auto'}
        ]
    )
    return result['secure_url']


def upload_order_attachment(file, order_id):
    """Order attachments → no crop, preserve original"""
    result = cloudinary.uploader.upload(
        file,
        folder="order_attachments",
        public_id=f"order_{order_id}_{file.name}",
        overwrite=False,  # keep all versions
        resource_type="auto"  # allows pdf, images etc
    )
    return result['secure_url']


def delete_image(public_id):
    """Delete from Cloudinary when record is deleted"""
    return cloudinary.uploader.destroy(public_id)