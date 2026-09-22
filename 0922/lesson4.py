import json
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any
from urllib.request import Request, urlopen

from tkintermapview import TkinterMapView


API_URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

DISPLAY_COLUMNS = {
    "sna": "站名",
    "sarea": "行政區",
    "ar": "地址",
    "mday": "更新時間",
    "Quantity": "車位總數",
    "available_rent_bikes": "可借車輛",
    "available_return_bikes": "可還車位",
}

COLUMN_WIDTHS = {
    "sna": 230,
    "sarea": 90,
    "ar": 300,
    "mday": 155,
    "Quantity": 90,
    "available_rent_bikes": 100,
    "available_return_bikes": 100,
}


def get_youbike_data():
    request = Request(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=15) as response:
        return json.load(response)


def show_station_details(root, station):
    station_name = station.get("sna", "").removeprefix("YouBike2.0_")
    try:
        latitude = float(station["latitude"])
        longitude = float(station["longitude"])
    except (KeyError, TypeError, ValueError):
        messagebox.showerror("地圖錯誤", "這個站點沒有有效的經緯度資料。", parent=root)
        return

    detail_window = tk.Toplevel(root)
    detail_window.title(f"站點資訊：{station_name}")
    detail_window.geometry("850x600")
    detail_window.transient(root)

    info_frame = ttk.Frame(detail_window, padding=15)
    info_frame.pack(fill="x")
    ttk.Label(info_frame, text=station_name, font=("TkDefaultFont", 16, "bold"))\
        .grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

    details = [
        ("行政區", station.get("sarea", "")),
        ("地址", station.get("ar", "")),
        ("更新時間", station.get("mday", "")),
        ("車位總數", station.get("Quantity", "")),
        ("可借車輛", station.get("available_rent_bikes", "")),
        ("可還車位", station.get("available_return_bikes", "")),
    ]
    for row, (label, value) in enumerate(details, start=1):
        ttk.Label(info_frame, text=f"{label}：").grid(row=row, column=0, sticky="w")
        ttk.Label(info_frame, text=value).grid(row=row, column=1, sticky="w")

    map_view = TkinterMapView(detail_window, corner_radius=0)
    map_view.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    map_view.set_position(latitude, longitude)
    map_view.set_zoom(16)
    map_view.set_marker(latitude, longitude, text=station_name)


def show_youbike_data(data):
    root = tk.Tk()
    root.title("YouBike 即時資料")
    root.geometry("1200x650")

    data_state = {"items": data}
    page_size = 50
    page_state = {"number": 0}
    columns = list(DISPLAY_COLUMNS)

    filter_frame = ttk.Frame(root, padding=(10, 10, 10, 5))
    filter_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
    filter_frame.grid_columnconfigure(3, weight=1)

    ttk.Label(filter_frame, text="行政區").grid(row=0, column=0, padx=(0, 5))
    district_var = tk.StringVar(value="全部")
    districts = sorted({station.get("sarea", "") for station in data})
    district_menu = ttk.Combobox(
        filter_frame,
        textvariable=district_var,
        values=["全部", *districts],
        state="readonly",
        width=12,
    )
    district_menu.grid(row=0, column=1, padx=(0, 15))

    ttk.Label(filter_frame, text="站名搜尋").grid(row=0, column=2, padx=(0, 5))
    search_var = tk.StringVar()
    search_entry = ttk.Entry(filter_frame, textvariable=search_var, width=25)
    search_entry.grid(row=0, column=3, sticky="ew", padx=(0, 10))

    result_label = ttk.Label(filter_frame, text=f"顯示 {len(data)} 個站點")
    result_label.grid(row=0, column=4, padx=(0, 15))
    ttk.Label(filter_frame, text="可借車輛欄位可點擊排序").grid(row=0, column=5)

    table = ttk.Treeview(root, columns=columns, show="headings")
    sort_state: dict[str, bool | None] = {"descending": None}
    visible_stations_state = {"items": []}

    pagination_frame = ttk.Frame(root, padding=(10, 5, 10, 10))
    pagination_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
    pagination_frame.grid_columnconfigure(1, weight=1)

    previous_button = ttk.Button(pagination_frame, text="上一頁")
    previous_button.grid(row=0, column=0, padx=(0, 10))
    page_label = ttk.Label(pagination_frame, text="第 1 頁 / 共 1 頁")
    page_label.grid(row=0, column=1)
    next_button = ttk.Button(pagination_frame, text="下一頁")
    next_button.grid(row=0, column=2, padx=(10, 0))
    detail_button = ttk.Button(pagination_frame, text="查看站點地圖")
    detail_button.grid(row=0, column=3, padx=(20, 5))
    update_button = ttk.Button(pagination_frame, text="立即更新")
    update_button.grid(row=0, column=4, padx=(5, 5))
    update_label = ttk.Label(pagination_frame, text="")
    update_label.grid(row=0, column=5, padx=(5, 0))
    countdown_state = {"seconds": 60, "after_id": None}

    def sort_by_rent_bikes():
        if sort_state["descending"] is None:
            sort_state["descending"] = True
        else:
            sort_state["descending"] = not sort_state["descending"]
        update_sort_heading()
        refresh_table(reset_page=True)

    def update_sort_heading():
        if sort_state["descending"] is None:
            heading = "可借車輛 ↕"
        elif sort_state["descending"]:
            heading = "可借車輛 ↓"
        else:
            heading = "可借車輛 ↑"
        table.heading("available_rent_bikes", text=heading)

    for column in columns:
        heading_options: dict[str, Any] = {"text": DISPLAY_COLUMNS[column]}
        if column == "available_rent_bikes":
            heading_options["text"] = "可借車輛 ↕"
            heading_options["command"] = sort_by_rent_bikes
        table.heading(column, **heading_options)
        table.column(column, width=COLUMN_WIDTHS[column], minwidth=70,
                     anchor="center" if column != "ar" and column != "sna" else "w")

    def update_pagination():
        total_pages = max(
            1, (len(visible_stations_state["items"]) + page_size - 1) // page_size
        )
        page_number = page_state["number"]
        page_label.configure(text=f"第 {page_number + 1} 頁 / 共 {total_pages} 頁")
        previous_button.configure(state="normal" if page_number > 0 else "disabled")
        next_button.configure(
            state="normal" if page_number + 1 < total_pages else "disabled"
        )

    def refresh_table(*_, reset_page=False):
        selected_district = district_var.get()
        keyword = search_var.get().strip().lower()

        visible_stations = []

        for station in data_state["items"]:
            station_name = station.get("sna", "").removeprefix("YouBike2.0_")
            matches_district = (
                selected_district == "全部"
                or station.get("sarea", "") == selected_district
            )
            matches_keyword = keyword in station_name.lower()

            if matches_district and matches_keyword:
                visible_stations.append((station, station_name))

        if sort_state["descending"] is not None:
            visible_stations.sort(
                key=lambda item: int(item[0].get("available_rent_bikes", 0) or 0),
                reverse=sort_state["descending"],
            )

        visible_stations_state["items"] = visible_stations
        if reset_page:
            page_state["number"] = 0

        total_pages = max(1, (len(visible_stations) + page_size - 1) // page_size)
        page_state["number"] = min(page_state["number"], total_pages - 1)
        start = page_state["number"] * page_size
        end = start + page_size

        table.delete(*table.get_children())
        for station, station_name in visible_stations[start:end]:
            values = [station.get(column, "") for column in columns]
            values[columns.index("sna")] = station_name
            table.insert("", tk.END, iid=station.get("sno", ""), values=values)

        result_label.configure(text=f"顯示 {len(visible_stations)} 個站點")
        update_pagination()

    def show_previous_page():
        if page_state["number"] > 0:
            page_state["number"] -= 1
            refresh_table()

    def show_next_page():
        total_pages = max(
            1, (len(visible_stations_state["items"]) + page_size - 1) // page_size
        )
        if page_state["number"] + 1 < total_pages:
            page_state["number"] += 1
            refresh_table()

    def show_selected_station():
        selection = table.selection()
        if not selection:
            messagebox.showinfo("提示", "請先選取一個站點。", parent=root)
            return

        station_id = selection[0]
        station = next(
            (item for item in data_state["items"] if item.get("sno") == station_id),
            None,
        )
        if station is not None:
            show_station_details(root, station)

    def update_data():
        update_button.configure(state="disabled")
        try:
            data_state["items"] = get_youbike_data()
            districts = sorted(
                {station.get("sarea", "") for station in data_state["items"]}
            )
            district_menu.configure(values=["全部", *districts])
            if district_var.get() not in ["全部", *districts]:
                district_var.set("全部")
            refresh_table()
            update_label.configure(text="資料已更新")
        except Exception as error:
            update_label.configure(text=f"更新失敗：{error}")
        finally:
            update_button.configure(state="normal")
            countdown_state["seconds"] = 60
            if countdown_state["after_id"] is not None:
                root.after_cancel(countdown_state["after_id"])
            countdown_state["after_id"] = root.after(60000, update_data)

    def update_countdown():
        seconds = countdown_state["seconds"]
        update_label.configure(text=f"下次自動更新：{seconds} 秒後")
        if seconds > 0:
            countdown_state["seconds"] -= 1
        root.after(1000, update_countdown)

    district_var.trace_add("write", lambda *_: refresh_table(reset_page=True))
    search_var.trace_add("write", lambda *_: refresh_table(reset_page=True))
    previous_button.configure(command=show_previous_page)
    next_button.configure(command=show_next_page)
    detail_button.configure(command=show_selected_station)
    update_button.configure(command=update_data)
    table.bind("<Double-1>", lambda _event: show_selected_station())
    table.bind("<Return>", lambda _event: show_selected_station())
    refresh_table(reset_page=True)

    y_scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
    x_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=table.xview)
    table.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    table.grid(row=1, column=0, sticky="nsew")
    y_scrollbar.grid(row=1, column=1, sticky="ns")
    x_scrollbar.grid(row=2, column=0, sticky="ew")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    countdown_state["after_id"] = root.after(60000, update_data)
    root.after(0, update_countdown)
    root.mainloop()


try:
    youbike_data = get_youbike_data()
    print(f"共取得 {len(youbike_data)} 筆資料")
    show_youbike_data(youbike_data)
except Exception as error:
    error_root = tk.Tk()
    error_root.withdraw()
    messagebox.showerror("取得資料失敗", str(error))
    error_root.destroy()