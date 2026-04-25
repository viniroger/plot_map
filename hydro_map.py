import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import osmnx as ox
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def get_water_bodies(bbox):
    """
    Busca corpos d'água no OpenStreetMap usando OSMnx.
    """
    print("Buscando corpos d'água no OSM (isso pode levar um tempo para áreas grandes)...")
    tags = {
        'natural': 'water',
        'waterway': ['riverbank', 'dock', 'canal', 'river'],
        'landuse': 'reservoir'
    }
    
    try:
        # OSMnx usa (left, bottom, right, top) -> (west, south, east, north)
        bbox_tuple = (bbox[2], bbox[0], bbox[3], bbox[1])
        water = ox.features_from_bbox(bbox_tuple, tags=tags)
        return water
    except Exception as e:
        print(f"Aviso: Não foi possível obter corpos d'água: {e}")
        return None

def create_hydro_map_v5(bbox, water_gdf, output_image):
    """
    Gera a visualização final: fontes extra grandes, mapa de localização ajustado
    e cores consistentes.
    """
    print("Gerando visualização final revisada...")
    
    # Definir cor do continente (verde claro)
    land_color = '#E8F5E9'
    
    fig = plt.figure(figsize=(18, 16))
    
    # Mapa Principal
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_facecolor(land_color)
    
    # Adicionar corpos d'água
    if water_gdf is not None and not water_gdf.empty:
        water_polygons = water_gdf[water_gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])]
        if not water_polygons.empty:
            water_polygons.plot(ax=ax, color='#4A7BB7', edgecolor='none', alpha=1.0, transform=ccrs.PlateCarree())
    
    # 1. Incluir um X vermelho extra grande na coordenada: lat. -3.21, lon. -60.6
    ax.text(-60.6, -3.21, 'X', color='red', fontsize=60, fontweight='bold', 
            ha='center', va='center', transform=ccrs.PlateCarree())
    
    # 2. Incluir texto "Manacapuru" extra grande na coordenada: -3.290918, -60.627429
    ax.text(-60.627429, -3.290918, 'Manacapuru', color='black', fontsize=28, 
            fontweight='bold', ha='right', va='top', transform=ccrs.PlateCarree(),
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=3))
    
    # 3. Incluir texto "Manaus" extra grande na coordenada: -3.073486, -60.010259
    ax.text(-60.010259, -3.073486, 'Manaus', color='black', fontsize=28, 
            fontweight='bold', ha='left', va='bottom', transform=ccrs.PlateCarree(),
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=3))
    
    # Configurações de eixos e limites do mapa principal
    ax.set_extent([bbox[2], bbox[3], bbox[0], bbox[1]], crs=ccrs.PlateCarree())
    
    # Aumentar fontes dos eixos (grade de coordenadas) - Extra Grande
    gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, linestyle='--', alpha=0.3)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 22, 'color': 'black', 'weight': 'bold'}
    gl.ylabel_style = {'size': 22, 'color': 'black', 'weight': 'bold'}
    
    # --- Mapa de Localização (América do Sul) ---
    # Ajustar posição para não cobrir o eixo X e começar no meio da imagem
    # [left, bottom, width, height]
    # Reduzindo o tamanho e subindo um pouco a base para liberar o eixo X
    # Ajustar posição e tamanho do mapa auxiliar: [left, bottom, width, height]
    # Começar no meio da imagem (bottom = 0.5 - height/2), mas ajustar para não cobrir o eixo X
    # Aumentar um pouco o width e height para melhor visualização
    ax_inset = fig.add_axes([0.68, 0.2, 0.2, 0.35], projection=ccrs.Orthographic(central_longitude=-60, central_latitude=-15))
    ax_inset.set_global()
    
    # Usar a mesma cor de continente da figura principal
    ax_inset.add_feature(cfeature.LAND, facecolor=land_color)
    ax_inset.add_feature(cfeature.OCEAN, facecolor='#E3F2FD')
    ax_inset.add_feature(cfeature.BORDERS, linestyle=':', alpha=0.5)
    ax_inset.add_feature(cfeature.COASTLINE, linewidth=0.5)
    
    # Limitar a visualização à América do Sul
    ax_inset.set_extent([-90, -30, -60, 15], crs=ccrs.PlateCarree())
    
    # Adicionar o retângulo vazado na área correspondente à imagem principal
    rect = Rectangle((bbox[2], bbox[0]), bbox[3]-bbox[2], bbox[1]-bbox[0],
                     linewidth=3, edgecolor='red', facecolor='none',
                     transform=ccrs.PlateCarree())
    ax_inset.add_patch(rect)
    
    # Salvar imagem final
    plt.savefig(output_image, bbox_inches='tight')
    print(f"Mapa final revisado salvo em: {output_image}")
    plt.close()

if __name__ == "__main__":
    # Região: Amazônia Central
    bbox = [-3.65, -2.91, -60.93, -59.80]
    
    MAP_IMAGE = "map_hydro.png"
    
    # 1. Obter corpos d'água
    water = get_water_bodies(bbox)
    
    # 2. Criar mapa final revisado
    create_hydro_map_v5(bbox, water, MAP_IMAGE)
