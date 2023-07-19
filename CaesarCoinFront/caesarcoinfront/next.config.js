/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,
  rewrites: async () => {
    return [
      {
        source: '/',
        destination: '/homepage/caesarcoinhome.html',
      },
      {
        source: '/caesarseed',
        destination: '/caesarseed/caesarseed.html',
      },
      {
        source: '/caesartorrent',
        destination: '/caesartorrent/caesartorrent.html',
      },
    ]
  },
}


module.exports = nextConfig
