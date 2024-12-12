use std::{collections::{HashMap, HashSet}, env, fs::File, io::{self, BufRead}, path::Path};

use itertools::Itertools;

type Garden = Vec<Vec<char>>;
type Plot = (usize, usize);

fn read_input(path: &Path) -> io::Result<Garden> {
    let file = File::open(path)?;

    let mut garden = Vec::new();
    for line in io::BufReader::new(file).lines() {
        garden.push(line?.chars().collect());
    }

    Ok(garden)
}

fn for_neighbours(plot: Plot, size: Plot, mut f: impl FnMut(Plot)) {
    if plot.0 > 0 { f((plot.0 - 1, plot.1)); }
    if plot.1 > 0 { f((plot.0, plot.1 - 1)); }
    if plot.0 + 1 < size.0 { f((plot.0 + 1, plot.1)); }
    if plot.1 + 1 < size.1 { f((plot.0, plot.1 + 1)); }
}

fn calc_region(garden: &Vec<Vec<char>>, size: Plot, start_plot: Plot) -> HashSet<Plot> {
    let plant = garden[start_plot.1][start_plot.0];
    let mut done_plots = HashSet::new();
    let mut todo_plots = HashSet::from([start_plot]);
    while let Some(plot) = todo_plots.iter().next() {
        let here = plot.clone();
        todo_plots.remove(&here);
        done_plots.insert(here);
        for_neighbours(here, size, |neighbour| {
            if !done_plots.contains(&neighbour) && garden[neighbour.1][neighbour.0] == plant {
                todo_plots.insert(neighbour);
            }
        });
    }
    done_plots
}

fn calc_perimeter(size: Plot, region: &HashSet<Plot>) -> usize {
    let mut perimeter = 4 * region.len();
    for plot in region.iter() {
        for_neighbours(*plot, size, |neighbour| {
            if region.contains(&neighbour) {
                perimeter -= 1;
            }
        });
    }
    perimeter
}

fn count_sides(region: &HashSet<Plot>, borders: &Vec<Plot>) -> usize {
    let mut sides = 0;
    let mut i = 0;
    let num_borders = borders.len();
    while i < num_borders {
        sides += 1;
        let inside = region.contains(&borders[i]);
        let (a, mut b) = borders[i];
        b += 1;
        i += 1;
        while i < num_borders && borders[i] == (a, b) && region.contains(&borders[i]) == inside {
            b += 1;
            i += 1;
        }
    }
    sides
}

fn calc_sides(region: &HashSet<Plot>) -> usize {
    let mut hborder_freqs = HashMap::new();
    let mut vborder_freqs = HashMap::new();
    for (x, y) in region.iter() {
        *hborder_freqs.entry((*x, *y)).or_insert(0usize) += 1;
        *hborder_freqs.entry((*x, *y + 1)).or_insert(0usize) += 1;
        *vborder_freqs.entry((*x, *y)).or_insert(0usize) += 1;
        *vborder_freqs.entry((x + 1, *y)).or_insert(0usize) += 1;
    }
    hborder_freqs.retain(|_, freq| *freq == 1);
    vborder_freqs.retain(|_, freq| *freq == 1);
    let hborders = hborder_freqs.iter().map(|((x, y), _)| (*y, *x)).sorted().collect();
    let vborders = vborder_freqs.iter().map(|((x, y), _)| (*x, *y)).sorted().collect();
    let flipped_region = HashSet::from_iter(region.iter().map(|(x, y)| (*y, *x)));
    count_sides(&flipped_region, &hborders) + count_sides(region, &vborders)
}

fn solve(garden: Garden) {
    let size = (garden[0].len(), garden.len());

    let mut done: HashSet<Plot> = HashSet::new();
    let mut total_cost1 = 0;
    let mut total_cost2 = 0;
    for y in 0..size.1 {
        for x in 0..size.0 {
            let plot = (x, y);
            if !done.contains(&plot) {
                let region = calc_region(&garden, size, plot);
                let area = region.len();
                let perimeter = calc_perimeter(size, &region);
                let sides = calc_sides(&region);
                total_cost1 += area * perimeter;
                total_cost2 += area * sides;
                done.extend(region.iter());
            }
        }
    }
    println!("part 1 total cost: {total_cost1}");
    println!("part 2 total cost: {total_cost2}");
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let garden = read_input(Path::new(&arg)).expect("reading input");
        solve(garden);
    }
}
