# Optimal Binary Search Tree (OBST)
## En İyi İkili Arama Ağacı

## 📋 Problem Nedir?

Normal Binary Search Tree'de yapı, elemanların eklenme sırasına bağlıdır. Peki **bazı anahtarların diğerlerinden daha sık arandığını** biliyorsak ne olur?

**Problem:** Erişim sıklıkları biliniyorken, ortalama arama süresini minimize eden BST nasıl oluşturulur?

### Örnek

```
Anahtarlar:  [10, 20, 30]
Frekanslar:  [1,  1,  10]  ← anahtar 30, 10 kat daha sık aranıyor!
```

**Normal BST:**
```
  10
    \
     20
       \
        30  ← en çok aranan, ama derinlik = 3!
```
**Maliyet:** 1×1 + 1×2 + 10×3 = **33 işlem**

**Optimal BST:**
```
     30  ← en çok aranan → kökde (derinlik = 1)
    /
   20
  /
10
```
**Maliyet:** 10×1 + 1×2 + 1×3 = **15 işlem**

✅ **Kazanç: 2.2x daha hızlı!**

---

## 🎯 Çözüm: Dinamik Programlama

### Formül

```
cost[i][j] = min(cost[i][r-1] + cost[r+1][j] + sum(freq[i..j]))
             r = kök indeksi (i'den j'ye)
```

**Açıklama:**
- Sol alt ağaç + Sağ alt ağaç + Tüm düğümler bir seviye aşağı

### Algoritma

```python
def optimal_bst(keys, freq, n):
    cost = [[0] * n for _ in range(n)]
    
    # Tek düğümlü ağaçlar
    for i in range(n):
        cost[i][i] = freq[i]
    
    # Alt ağaç uzunluklarını dene
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float('inf')
            freq_sum = sum(freq[i:j+1])
            
            # Her düğümü kök olarak dene
            for r in range(i, j + 1):
                left = cost[i][r-1] if r > i else 0
                right = cost[r+1][j] if r < j else 0
                c = left + right + freq_sum
                
                if c < cost[i][j]:
                    cost[i][j] = c
    
    return cost[0][n-1]
```

### Karmaşıklık
- **Zaman:** O(n³) - üç iç içe döngü
- **Alan:** O(n²) - cost tablosu

---

## ⚡ BST vs OBST Karşılaştırması

| Özellik | BST | OBST |
|---------|-----|------|
| **Oluşturma** | O(n log n) | O(n³) |
| **Frekans desteği** | ❌ | ✅ |
| **Arama süresi** | O(log n) - O(n) | Optimal |
| **Yapı** | Ekleme sırasına bağlı | Frekanslara göre optimal |
| **Dinamik güncelleme** | ✅ Kolay | ❌ Zor |
| **Ne zaman kullan** | Frekanslar bilinmiyor | Frekanslar biliniyor |

---

## 💡 Avantajlar

✅ **Minimum ortalama arama süresi** - Verilen frekanslar için matematiksel olarak optimal  
✅ **Öngörülebilir performans** - Worst-case degradasyon yok  
✅ **Statik veriler için ideal** - Bir kez oluştur, sürekli kullan  

## ❌ Dezavantajlar

❌ **Yavaş oluşturma** - O(n³) hesaplama gerekir  
❌ **Statik yapı** - Güncelleme pahalı  
❌ **Frekans gereksinimi** - Önceden istatistik bilinmeli  

---

## 📊 Kullanım Alanları

### ✅ Ne zaman kullanılır:

- 🗄️ **Veritabanı indeksleri** - Bilinen sorgu istatistikleri
- 🔤 **Derleyiciler** - Anahtar kelimelerin frekans dağılımı biliniyor
- 📚 **Sözlükler** - Kelimelerin kullanım sıklıkları farklı
- 🌐 **DNS önbellek** - Popüler domainler var
- 🔍 **Arama sistemleri** - Sorgu dağılımı biliniyor

### ❌ Ne zaman kullanılmaz:

- Veriler sürekli değişiyor
- Frekanslar bilinmiyor veya eşit
- Hızlı oluşturma gerekiyor

---

## 🔑 Temel Farklar

### Maliyet Hesaplama

**BST:**
- Maliyet şansa bağlı (ekleme sırasına göre)
- Worst case: O(n)
- Best case: O(log n)

**OBST:**
- Maliyet = Σ(freq[i] × depth[i])
- Her zaman optimal
- Garantili performans

### Oluşturma

**BST:** Dinamik - elemanlar sırayla eklenir  
**OBST:** Statik - tüm veriler önceden biliniyor, tek seferde oluşturulur

---

## 📈 Görsel Örnek

```
Anahtarlar:  [A,  B,  C,  D]
Frekanslar:  [5, 10,  3,  2]
```

**Normal BST (sıralı):**
```
    A
      \
       B  ← En sık kullanılan çok derinde!
         \
          C
            \
             D

Maliyet = 5×1 + 10×2 + 3×3 + 2×4 = 42
```

**Optimal BST:**
```
       B  ← En sık kullanılan kökde
      / \
     A   C
           \
            D

Maliyet = 10×1 + 5×2 + 3×2 + 2×3 = 32
```

**Kazanç: %24 daha hızlı! 🚀**

---

## 🎓 Özet

- OBST, bilinen frekanslar için optimal arama süresini garanti eder
- Dinamik programlama ile O(n³) zamanda çözülür
- Statik veriler için mükemmel, dinamik veriler için uygun değil
- **Temel prensip:** Sık kullanılan anahtarlar köke yakın → daha hızlı erişim ⚡