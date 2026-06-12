import { useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN

type ProfileMapProps = {
  lat: number
  lng: number
  className?: string
}

export function ProfileMap({ lat, lng, className = '' }: ProfileMapProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<mapboxgl.Map | null>(null)

  useEffect(() => {
    if (!MAPBOX_TOKEN || !containerRef.current) return

    mapboxgl.accessToken = MAPBOX_TOKEN

    const map = new mapboxgl.Map({
      container: containerRef.current,
      style: 'mapbox://styles/mapbox/dark-v11',
      center: [lng, lat],
      zoom: 12,
      interactive: true,
      attributionControl: true,
    })

    map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'top-right')

    new mapboxgl.Marker({ color: '#c9a227' }).setLngLat([lng, lat]).addTo(map)

    mapRef.current = map

    return () => {
      map.remove()
      mapRef.current = null
    }
  }, [lat, lng])

  if (!MAPBOX_TOKEN) {
    return (
      <div
        className={`flex items-center justify-center rounded-xl border border-border bg-canvas px-4 py-8 text-center text-sm text-muted ${className}`}
      >
        Set <code className="text-accent">VITE_MAPBOX_ACCESS_TOKEN</code> in{' '}
        <code className="text-accent">frontend/.env</code> to show the map.
      </div>
    )
  }

  return (
    <div
      ref={containerRef}
      className={`h-48 overflow-hidden rounded-xl border border-border ${className}`}
      role="img"
      aria-label="Map showing your saved location"
    />
  )
}
