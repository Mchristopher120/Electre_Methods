import React from 'react'
import { Grid, TextField } from '@mui/material'

export default function ParamInputs({params, onChange}){
  // params is object of name->value
  const handle = (k, v) => onChange({...params, [k]: v})
  return (
    <Grid container spacing={2}>
      {Object.keys(params).map(k => (
        <Grid item key={k}>
          <TextField label={k} size="small" value={params[k]} onChange={e => handle(k, e.target.value)} />
        </Grid>
      ))}
    </Grid>
  )
}
