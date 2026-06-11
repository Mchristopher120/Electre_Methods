import React from 'react'
import { TextField, Grid } from '@mui/material'

export default function MatrixEditor({rows, cols, value, onChange}){
  // value: array of arrays
  const handleCell = (r,c, v) => {
    const copy = value.map(row => row.slice())
    copy[r][c] = v
    onChange(copy)
  }

  return (
    <Grid container spacing={1}>
      {Array.from({length: rows}).map((_, r) => (
        <Grid item xs={12} key={r}>
          <div style={{display:'flex', gap:8}}>
            {Array.from({length: cols}).map((__, c) => (
              <TextField size="small" key={c} value={(value[r] && value[r][c]) ?? ''}
                onChange={e => handleCell(r,c, e.target.value)} style={{width:100}} />
            ))}
          </div>
        </Grid>
      ))}
    </Grid>
  )
}
