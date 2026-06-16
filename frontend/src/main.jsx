import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { Container, AppBar, Toolbar, Typography, Button } from '@mui/material'
import ElectreIPage from './pages/ElectreIPage'
import ElectreISPage from './pages/ElectreISPage'
import ElectreIVPage from './pages/ElectreIVPage'
import ElectreIIPage from './pages/ElectreIIPage'
import ElectreIIIPage from './pages/ElectreIIIPage'
import ElectreTriPage from './pages/ElectreTriPage'
import axios from 'axios'
axios.defaults.baseURL = 'https://j-electre-api.onrender.com'

function App(){
  return (
    <BrowserRouter>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>J-ELECTRE</Typography>
          <Button color="inherit" component={Link} to="/ei">EI</Button>
          <Button color="inherit" component={Link} to="/ei_s">EI_s</Button>
          <Button color="inherit" component={Link} to="/ei_v">EI_v</Button>
          <Button color="inherit" component={Link} to="/eii">EII</Button>
          <Button color="inherit" component={Link} to="/eiii">EIII</Button>
          <Button color="inherit" component={Link} to="/eiv">EIV</Button>
          <Button color="inherit" component={Link} to="/etri">ETri</Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 3 }}>
        <Routes>
          <Route path="/" element={<ElectreIPage/>} />
          <Route path="/i" element={<ElectreIPage/>} />
          <Route path="/i_s" element={<ElectreISPage/>} />
          <Route path="/i_v" element={<ElectreIVPage/>} />
          <Route path="/ii" element={<ElectreIIPage/>} />
          <Route path="/iii" element={<ElectreIIIPage/>} />
          <Route path="/iv" element={<ElectreIVPage/>} />
          <Route path="/tri" element={<ElectreTriPage/>} />

          {/* Keep legacy routes and add 'e' prefixed routes for compatibility */}
          <Route path="/ei" element={<ElectreIPage/>} />
          <Route path="/ei_s" element={<ElectreISPage/>} />
          <Route path="/ei_v" element={<ElectreIVPage/>} />
          <Route path="/eii" element={<ElectreIIPage/>} />
          <Route path="/eiii" element={<ElectreIIIPage/>} />
          <Route path="/eiv" element={<ElectreIVPage/>} />
          <Route path="/etri" element={<ElectreTriPage/>} />
        </Routes>
      </Container>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')).render(<App />)
