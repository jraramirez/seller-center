from product.models import Variations

def hasVariations(row):
  for i in range(0,7):
    if(row['variation'+str(i+1)+'_id'] == row['variation'+str(i+1)+'_id'] or \
      row['variation'+str(i+1)+'_price'] == row['variation'+str(i+1)+'_price']  or \
      row['variation'+str(i+1)+'_stock'] == row['variation'+str(i+1)+'_stock']  or \
      row['variation'+str(i+1)+'_name'] == row['variation'+str(i+1)+'_name']
    ):
      return True
  return False