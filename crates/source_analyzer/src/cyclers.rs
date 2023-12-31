use std::{
    collections::{HashMap, HashSet},
    path::Path,
};

use serde::Deserialize;
use topological_sort::TopologicalSort;

use crate::{
    contexts::Field,
    error::Error,
    manifest::{CyclerManifest, FrameworkManifest},
    node::Node,
};

pub type CyclerName = String;
pub type InstanceName = String;
pub type OutputName = String;

#[derive(Debug)]
pub struct Cyclers {
    pub cyclers: Vec<Cycler>,
}

impl Cyclers {
    pub fn try_from_manifest(
        manifest: FrameworkManifest,
        root: impl AsRef<Path>,
    ) -> Result<Cyclers, Error> {
        let cyclers = manifest
            .cyclers
            .into_iter()
            .map(|manifest| Cycler::try_from_manifest(manifest, root.as_ref()))
            .collect::<Result<_, _>>()?;
        Ok(Self { cyclers })
    }

    pub fn sort_nodes(&mut self) -> Result<(), Error> {
        for cycler in &mut self.cyclers {
            cycler.sort_nodes()?;
        }
        Ok(())
    }

    pub fn number_of_instances(&self) -> usize {
        self.cyclers
            .iter()
            .map(|cycler| cycler.instances.len())
            .sum()
    }

    pub fn instances(&self) -> impl Iterator<Item = (&Cycler, &InstanceName)> {
        self.cyclers.iter().flat_map(move |cycler| {
            cycler
                .instances
                .iter()
                .map(move |instance| (cycler, instance))
        })
    }

    pub fn instances_with(
        &self,
        kind: CyclerKind,
    ) -> impl Iterator<Item = (&Cycler, &InstanceName)> {
        self.cyclers
            .iter()
            .filter(move |cycler| cycler.kind == kind)
            .flat_map(move |cycler| {
                cycler
                    .instances
                    .iter()
                    .map(move |instance| (cycler, instance))
            })
    }

    pub fn watch_paths(&self) -> impl Iterator<Item = &Path> {
        self.cyclers.iter().flat_map(|cycler| {
            cycler
                .setup_nodes
                .iter()
                .chain(cycler.cycle_nodes.iter())
                .map(|node| node.file_path.as_path())
        })
    }
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, PartialEq)]
pub enum CyclerKind {
    Perception,
    RealTime,
}

#[derive(Debug)]
pub struct Cycler {
    pub name: CyclerName,
    pub kind: CyclerKind,
    pub instances: Vec<InstanceName>,
    pub setup_nodes: Vec<Node>,
    pub cycle_nodes: Vec<Node>,
}

impl Cycler {
    fn try_from_manifest(cycler_manifest: CyclerManifest, root: &Path) -> Result<Cycler, Error> {
        let instances = cycler_manifest
            .instances
            .iter()
            .map(|instance_name| format!("{}{}", cycler_manifest.name, instance_name))
            .collect();
        let setup_nodes = cycler_manifest
            .setup_nodes
            .iter()
            .map(|specification| Node::try_from_node_name(specification, root))
            .collect::<Result<Vec<_>, _>>()?;
        let cycle_nodes = cycler_manifest
            .nodes
            .iter()
            .map(|specification| Node::try_from_node_name(specification, root))
            .collect::<Result<Vec<_>, _>>()?;

        Ok(Cycler {
            name: cycler_manifest.name.to_string(),
            kind: cycler_manifest.kind,
            instances,
            setup_nodes,
            cycle_nodes,
        })
    }

    pub fn sort_nodes(&mut self) -> Result<(), Error> {
        let output_name_to_setup_node: HashMap<_, _> = self
            .setup_nodes
            .iter()
            .flat_map(|node| {
                node.contexts
                    .main_outputs
                    .iter()
                    .filter_map(move |field| match field {
                        Field::MainOutput { name, .. } => Some((name.to_string(), node)),
                        _ => None,
                    })
            })
            .collect();
        let sorted_setup_nodes = sort_nodes(
            &self.setup_nodes,
            &output_name_to_setup_node,
            &HashSet::new(),
        )?;

        let setup_output_names = output_name_to_setup_node.keys().cloned().collect();
        let output_to_node: HashMap<_, _> = self
            .cycle_nodes
            .iter()
            .flat_map(|node| {
                node.contexts
                    .main_outputs
                    .iter()
                    .filter_map(move |field| match field {
                        Field::MainOutput { name, .. } => Some((name.to_string(), node)),
                        _ => None,
                    })
            })
            .collect();
        let sorted_cycle_nodes =
            sort_nodes(&self.cycle_nodes, &output_to_node, &setup_output_names)?;

        self.setup_nodes = sorted_setup_nodes;
        self.cycle_nodes = sorted_cycle_nodes;
        Ok(())
    }

    pub fn iter_nodes(&self) -> impl Iterator<Item = &Node> {
        self.setup_nodes.iter().chain(self.cycle_nodes.iter())
    }
}

fn sort_nodes(
    nodes: &[Node],
    output_to_node: &HashMap<String, &Node>,
    existing_output_names: &HashSet<OutputName>,
) -> Result<Vec<Node>, Error> {
    let mut topological_sort = TopologicalSort::<&Node>::new();
    for node in nodes {
        topological_sort.insert(node);
        for dependency in node
            .contexts
            .cycle_context
            .iter()
            .filter_map(|field| match field {
                Field::HistoricInput { path, .. }
                | Field::Input {
                    path,
                    cycler_instance: None,
                    ..
                }
                | Field::RequiredInput {
                    path,
                    cycler_instance: None,
                    ..
                } => {
                    let first_segment = path.segments.first()?;
                    Some(first_segment.name.as_str())
                }
                _ => None,
            })
        {
            let producing_node = match output_to_node.get(dependency) {
                Some(node) => node,
                None if existing_output_names.contains(dependency) => continue,
                None => {
                    return Err(Error::MissingOutput {
                        node: node.name.clone(),
                        output: dependency.to_string(),
                    })
                }
            };
            topological_sort.add_dependency(*producing_node, node);
        }
    }

    let sorted_nodes = topological_sort.by_ref().cloned().collect();
    if !topological_sort.is_empty() {
        return Err(Error::CircularDependency);
    }

    Ok(sorted_nodes)
}
