import React from 'react'

export default function Heatmap({matrix, labels, width=400, height=400}){
  if(!matrix) return <div>No matrix data</div>
  const n = matrix.length
  const cellW = width / n
  const cellH = height / n
  // find max for normalization
  let max = 0
  for(let i=0;i<n;i++) for(let j=0;j<n;j++) if(Math.abs(matrix[i][j])>max) max = Math.abs(matrix[i][j])
  if(max === 0) max = 1

  return (
    <svg width={width} height={height} style={{border:'1px solid #ddd'}}>
      {matrix.map((row,i)=>row.map((v,j)=>{
        const val = Math.abs(v)/max
        const color = `rgba(136,132,216,${val})`
        return (
          <g key={`${i}-${j}`}>
            <rect x={j*cellW} y={i*cellH} width={cellW} height={cellH} fill={color} stroke="#fff" />
            <title>{`(${i+1},${j+1}) = ${v}`}</title>
          </g>
        )
      }))}
    </svg>
  )
}
