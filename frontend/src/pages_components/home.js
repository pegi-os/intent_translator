import React from 'react'
export default function Home() {
  return (
    <div >
        <div style={{
          position: 'absolute',
          top: '30%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center',
          }}>
        <img src={require('../dublinfig.jpeg')} alt="Dublin" style={{ maxWidth: '100%', height: 'auto' }} />
        
        </div>
          
    </div>
  )
}
