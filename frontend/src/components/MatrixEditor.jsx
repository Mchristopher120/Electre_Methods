import React from 'react'
import { TextField, Grid } from '@mui/material'

export default function MatrixEditor({ rows, cols, value, onChange }) {
  // value: array of arrays
  const handleCell = (r, c, v) => {
    // 1. Cria uma cópia profunda garantindo que todas as linhas necessárias existam
    const copy = Array.from({ length: rows }).map((_, rowIndex) => {
      // Se a linha já existe no valor original, nós a copiamos. 
      // Se não, criamos uma nova linha vazia com o número certo de colunas.
      if (value[rowIndex]) {
        return [...value[rowIndex]];
      }
      return Array(cols).fill('');
    });

    // 2. Atualiza o valor específico
    copy[r][c] = v;

    // 3. Devolve a matriz inteira atualizada
    onChange(copy);
  }

  return (
    <Grid container spacing={1}>
      {Array.from({ length: rows }).map((_, r) => (
        <Grid item xs={12} key={`row-${r}`}>
          <div style={{ display: 'flex', gap: 8 }}>
            {Array.from({ length: cols }).map((_, c) => (
              <TextField
                size="small"
                key={`cell-${r}-${c}`}
                value={(value[r] && value[r][c]) ?? ''}
                onChange={e => handleCell(r, c, e.target.value)}
                style={{ width: 100 }}
              />
            ))}
          </div>
        </Grid>
      ))}
    </Grid>
  )
}