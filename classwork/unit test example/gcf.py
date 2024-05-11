def func( m, n ): #gcf, assume m and n are real numbers
   while n != 0:
      r = m % n
      m = n
      n = r

   return m