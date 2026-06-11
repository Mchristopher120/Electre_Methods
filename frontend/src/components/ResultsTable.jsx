import React from 'react'
import { Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material'

export default function ResultsTable({data}){
  // data: array of rows arrays
  return (
    <Paper>
      <Table size="small">
        <TableBody>
          {data.map((row, i) => (
            <TableRow key={i}>
              {row.map((cell, j) => (
                <TableCell key={j}>{cell}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  )
}
