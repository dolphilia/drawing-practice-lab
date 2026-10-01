/* v1: only endpoint arithmetic; no automatic detection. */
function measureRatio(points) {
  if (points.length !== 6 || points.some(p => p.length !== 2 || p.some(v => !Number.isFinite(v))))
    throw new Error('6点の有限座標が必要です');
  const top=(points[0][1]+points[1][1])/2;
  const join=(points[2][1]+points[3][1])/2;
  const bottom=(points[4][1]+points[5][1])/2;
  const upper=join-top, lower=bottom-join;
  if (upper<=0 || lower<=0) throw new Error('高さが非正です：欠測理由を記録してください');
  const ratio=lower/upper;
  return {upper,lower,ratio,signed_error:ratio-.75,absolute_error:Math.abs(ratio-.75)};
}
if (typeof module !== 'undefined') module.exports={measureRatio};
